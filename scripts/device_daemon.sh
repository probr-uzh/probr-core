#!/usr/bin/env sh

# This subhell/sourced detection MUST be executed as the very first statement
# See below for detailed documentation
is_sourced() {
  [ "$_" != "$0" ]
  echo $?
}
SOURCE_DETECTED=$(is_sourced)

#### BEGIN Global variables ####
VERSION='0.3.0'
SCRIPT_NAME='device_daemon.sh'
PID_FILE='device_daemon.pid'
API_KEY_FILE='api.key'
BASE_URL='https://probr.sook.ch'
# BASE_URL='http://localhost:8080'
# Time to sleep before starting in seconds
# waiting for network/internet to become available
SLEEP_ON_STARTUP=0
# Time between two status requests in seconds
SLEEP_PERIOD=5

## Server constants
STATUS_NOT_YET_EXECUTED=0
STATUS_EXECUTING=1
STATUS_EXECUTED=2

## Debug mode (true|false)
DEBUG=false
AUTO_DETECT_SOURCED=true
TRACE=false
POSIX_COMPATIBLE=false
## Proxy (yes|no)
PROXY=no
HTTP_PROXY=localhost:8888
HTTPS_PROXY=$HTTP_PROXY
#### END Global variables ####

# Determines whether the script is run in a subshell or in the same process.
# Note:
#   This check is not fully portable. Although being syntactically correct, it
#   returns subshell instead of source when used in certain shell types (e.g., sh, ash)
#   Use the global flag $SOURCED to force using sourced mode.
# Returns:
#   0 if the scripts runs in a subshell or within a non-compatible shell
#   1 if the function runs in the same process (i.e., script has been sourced)
# is_subshell() {
#   See above for documentation
# }

setup_debug_mode() {
  if [ "$DEBUG" == 'true' ]; then
    # Exit if a command fails (the same as `set -e`)
    set -o errexit
    # Exit if a command within a pipe fails
    set -o pipefail
    # Exit if an uninitialised variable is used (the same as `set -u`)
    set -o nounset

    if [ "$TRACE" == 'true' ]; then
      # Print trace of every command
      set -x
    fi

    if [ "$POSIX_COMPATIBLE" != 'true' ]; then
    # Exit on errors in other functions or via the time command [POSIX incompatible]
    set -o errtrace

    # Error handler for debugging purpose based on http://stackoverflow.com/a/185900
    error() {
      local parent_lineno="$1"
      local message="${2:-}"
      # default to '1' if exit code not explicitly given
      local code="${3:-1}"
      if [ -n "$message" ] ; then
        echo "Error on or near line ${parent_lineno}: ${message}; exiting with status ${code}"
      else
        echo "Error on or near line ${parent_lineno}; exiting with status ${code}"
      fi
      exit "${code}"
    }
    # Trap exits triggered by errexit [POSIX incompatible]
    trap 'error ${LINENO}' ERR
    fi
  fi
}

cd_into_script_dir() {
  local basedir
  basedir=$(dirname $0)
  cd $basedir
}

# clean_up() {
#     # You might want to do cleanup tasks here
#     echo "Exiting ..."
#     exit
# }
# ATTENTION: This trap breaks the trap on remote command execution (submit_result)
# Run every time when the script exists (e.g., via CTRL + C)
#  except on non-catchable signals (e.g., SIGKILL=9)
# trap 'clean_up' EXIT


# Performs a wget http request to the probr server
# Arguments:
#   probr url suffix
#   wget options (optional)
# Returns:
#   http response
# Example:
#   base_wget '/api-device/statuses/' --header 'Accept: text/plain'
base_wget() {
  local url_suffix="$1"
  shift
  wget --output-document=- \
       --header "Api-Key: $(api_key)" \
       --quiet \
       --execute use_proxy=$PROXY \
       --execute http_proxy=$HTTP_PROXY \
       --execute https_proxy=$HTTPS_PROXY \
       "$@" \
       -- "${BASE_URL}${url_suffix}"
}

# Performs an http get request to the probr server
# Arguments:
#   probr url suffix
#   wget options (optional)
# Returns:
#   http response
# Exampe:
#   get 'api/commands/'
get() {
  local url_suffix="$1"
  shift
  base_wget "$url_suffix" \
                --header 'Accept: text/plain' \
                "$@"
}

# Performs an http post request with json payload to the probr server
# Arguments:
#   probr url suffix
#   json body data
#   wget options (optional)
# Returns:
#   http response
# Example:
#   post '/api-device/statuses/' '{"cpu_load": "0.4"}'
post() {
  local url_suffix="$1"
  local post_data="$2"
  shift 2
  base_wget "$url_suffix" \
                --header 'Content-Type: application/json' \
                --post-data="$post_data" \
                "$@"
}

download_script() {
  get "/static/${SCRIPT_NAME}" > "${SCRIPT_NAME}.new"
}

update_script() {
  download_script && cp "${SCRIPT_NAME}.new" "${SCRIPT_NAME}" && exec "./${SCRIPT_NAME}"
}

device_status() {
  total_memory=$(top -bn1 | awk '/KiB Mem/ { print $3 };')
  used_memory=$(top -bn1 | awk '/KiB Mem/ { print $5 };')
  total_disk=$(df -k . | awk 'NR==2 { print $4 };')
  used_disk=$(df -k . | awk 'NR==2 { print $3 };')
  cpu_load=$(top -bn2 | awk '/Cpu/ { print 100 - $8};' | tail -n1)

  echo '{"cpu_load":"'$cpu_load'","used_disk":"'$used_disk'","total_disk":"'$total_disk'","used_memory":"'$used_memory'","total_memory":"'$total_memory'"}'
}

fake_device_status() {
  echo '{"cpu_load":"0.3","used_disk":"10","total_disk":"20","used_memory":"256","total_memory":"2048"}' 
}

post_status() {
    response=$(post '/api-device/statuses/' "$(device_status)")

    if [ -n "$response" ]; then
        echo "Successfully posted status: $response"
    else
        echo "Error during posting status. Got response: $response"
    fi
}

api_key() {
  cat "$API_KEY_FILE"
}

set_api_key() {
  local api_key=$1
  echo "${api_key}" > $API_KEY_FILE
}

command_file() {
  local command_uuid=$1
  echo "./commands/${command_uuid}.sh"
}

command_log_file() {
  local command_uuid=$1
  echo "./commands/${command_uuid}.log"
}

command_pid_file() {
  local command_uuid=$1
  echo "./commands/${command_uuid}.pid"
}

command_pid() {
  local command_uuid=$1
  cat $(command_pid_file "$command_uuid")
}

# Arguments:
#   command uuid
#   status: defined in `probr-core/devices/models.py COMMAND_STATUS_CHOICES`
#             use constants `STATUS_NOT_YET_EXECUTED`, `STATUS_EXECUTING`, `STATUS_EXECUTED`
set_command_status() {
  post "/api-device/commands/$1/" '{"status":"'$2'"}'
}

non_executed_commands() {
  get "/api-device/commands/?status=${STATUS_NOT_YET_EXECUTED}"
}

submit_result() {
  local command_uuid=$1
  local log_file=$2
  tmp_file="${log_file}.upload"
  # We need to make a copy of the log file, because curl can't handle the still opened log file
  cp "$log_file" "$tmp_file"
  base_wget "/api-device/commands/${command_uuid}/" --post-file="$tmp_file"
  rm "$tmp_file"
}

# Callback function when exiting a background command
finished_command() {
  local command_uuid=$1
  # TODO: Why do we first submit the result and then pkill the child processes and not vice versa?
  # Consider that there is a race condition: finished_command requires that that pid was already written to the .pid file !!!
  submit_result "$command_uuid" "$(command_log_file "$command_uuid")"
  # Kill own child processes. This will exit with non-zero value if the process already finished.
  pkill -P $(command_pid "$command_uuid")
  # Clean up all command-related files
  rm ./commands/${command_uuid}*
  exit
}

# Note:
#   Depends on the `finished_command` callback function using a trap on script exit
#   Instead of executing the command within its own subprocess with ./COMMAND.sh,
#   we are using source to run it within the same process such that can kill the
#   childprocess later.
execute_in_background() {
  local command_file=$1
  local log_file=$2
  local command_uuid=$3
  (trap "finished_command ${command_uuid}" EXIT && source ${command_file}) >${log_file} 2>&1 </dev/null &
  # Write pid of the most recently executed background process to file and stdout
  echo $! | tee "$(command_pid_file "$command")"
}

execute_commands() {
  mkdir -p commands
  for command in $(non_executed_commands); do
    cmd_file=$(command_file "$command")
    echo "Downloading command $command ..."
    get "/api-device/commands/${command}" > "$cmd_file"
    chmod +x "$cmd_file"
    echo "Starting command $command ..."
    set_command_status "$command" "$STATUS_EXECUTING"

    # Execute script, while piping all output to a log file
    pid=$(execute_in_background "$cmd_file" "$(command_log_file "$command")" "$command")
    echo "Started command ${command} with pid ${pid}"
  done
}

infinite_loop() {
  while :
  do
      echo "Infinite loop [hit CTRL+C to stop]"
      post_status
      execute_commands
      sleep $SLEEP_PERIOD
  done
}

save_pid() {
  echo $$ > "$PID_FILE"
}

# Arguments:
#   api key (mandatory only on first execution; can be overwritten later)
main() {
  local api_key="$1"

  save_pid
  sleep $SLEEP_ON_STARTUP

  if [ -n "$api_key" ]; then
    set_api_key "$api_key"
  fi

  if [ -s "$API_KEY_FILE" ]; then
    echo "Using api key \"$(api_key)\""
    infinite_loop
  else
    echo "No api key available. Please provide an api key as script argument."
    exit 1
  fi
}

# TODO: Does && really don't work cross-platform?
# => remember compatibility blog
# => test on different platforms
if [ \( "$AUTO_DETECT_SOURCED" == 'true' \) -a \( "$SOURCE_DETECTED" == "0" \) ]; then
  # When this script is sourced $0 contains no path (e.g., -bash)
  echo "pwd=$(pwd)"
else
  # Make the script working from any current working directory
  cd_into_script_dir
  setup_debug_mode
  # Pass original parameters to main function
  main "$@"
fi
