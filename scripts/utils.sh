#!/usr/bin/env sh

#### BEGIN Global variables ####
VERSION='0.4.1'
SCRIPT_NAME='device_daemon.sh'
PID_FILE='device_daemon.pid'
API_KEY_FILE='api.key'
BASE_URL_FILE='probr.url'

# Time to sleep before starting in seconds
# waiting for network/internet to become available
SLEEP_ON_STARTUP=20
# Time between two status requests in seconds
SLEEP_PERIOD=5

## Server constants
STATUS_NOT_YET_EXECUTED=0
STATUS_EXECUTING=1
STATUS_EXECUTED=2

## Debug options (true|false)
SETUP_CRONJOB=true
DEBUG=false
AUTO_DETECT_SOURCED=false
TRACE=false
POSIX_COMPATIBLE=false
## Proxy (yes|no)
PROXY=no
HTTP_PROXY=localhost:8888
HTTPS_PROXY=$HTTP_PROXY
#### END Global variables ####

setup_debug_mode() {
  if [ "$DEBUG" = 'true' ]; then
    # Exit if a command fails (the same as `set -e`)
    set -o errexit
    # Exit if a command within a pipe fails
    set -o pipefail
    # Exit if an uninitialised variable is used (the same as `set -u`)
    set -o nounset

    if [ "$TRACE" = 'true' ]; then
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
    # trap 'error ${LINENO}' ERR
    fi
  fi
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
       "$@" \
       -- "$(base_url)${url_suffix}"
       # Older versions of wget doesn't support this option
       # Check whether these older wget versions work at all
       # --execute use_proxy=$PROXY \
       # --execute http_proxy=$HTTP_PROXY \
       # --execute https_proxy=$HTTPS_PROXY \
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
  local script="$1"
  get "/static/${script}" > "${script}.new"
}

replace_script() {
  local script="$1"
  cp "${script}.new" "${script}"
  chmod +x "${script}"
  rm "${script}.new"
}

save_pid() {
  echo $$ > "$PID_FILE"
}

get_pid() {
  cat "$PID_FILE"
}

# TODO: Remove because this doesn't work from within a remote command
#       The device script would be killed when this command exits
restart_device_daemon() {
  old_pid=$(get_pid)
  kill $old_pid
  nohup ./device_daemon.sh >/dev/null 2>&1 </dev/null &
  echo $!
  sleep 20
}

update_scripts() {
  download_script "utils.sh" &&
  download_script "device_daemon.sh"
}

# Apply update if a new version of the device deamon is available
check_for_updates() {
  if [ -s "utils.sh.new" ] && [ -s "device_daemon.sh.new" ]; then
    echo "Updating scripts ..."
    replace_script "utils.sh" &&
    replace_script "device_daemon.sh" &&
    exec "./device_daemon.sh"
  fi
}

total_memory() {
  free -m | awk 'NR==2 {print $2};'
}

used_memory() {
  free -m | awk 'NR==2 {print $3};'
}

total_disk() {
  df -k . | awk 'NR==2 { print $4 };'
}

used_disk() {
  df -k . | awk 'NR==2 { print $3 };'
}

# Examples:
# echo "CPU:   0% usr   0% sys   0% nic 100% idle   0% io   0% irq   0% sirq" | extract_idle_time => 100
# echo "%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st" | extract_idle_time => 100.0
# echo "%Cpu(s): 60.9 us,  0.0 sy,  0.0 ni, 39.1 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st" | extract_idle_time => 39.1
# echo "%Cpu(s):100.0 us,  0.0 sy,  0.0 ni,  0.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st" | extract_idle_time => 0.0
extract_idle_time() {
  sed -n 's/.*[^0-9]\([0-9]\+.\?[0-9]\+\)\%\? id.*/\1/p'
}

# An alternative would be to consider cpu core normalized load averages over 1 minute (see http://www.rackspace.com/knowledge_center/article/checking-system-load-on-linux)
# NOTE: This command blocks and needs to wait for 1 second until the value is available
# NOTE: Not Mac OS X compatible
# Explanation:
# Must ignore the first invalid value => therefore -n2 (according to http://stackoverflow.com/a/4940972 and http://linux.die.net/man/1/top)
# Double grep prevents including the grep process itself
# Tail only takes the second value and ignores the first
# Awk inverts the idle time (taking steal time into consideration)
# Sed removes the percentage sign '%' which is included in certain distributions (e.g. OpenWrt)
cpu_load() {
  top -b -n2 -d1 | grep -i "cpu" | grep "id" | tail -n+2 | extract_idle_time | awk '{ print 100 - $1 }' | sed 's/%//'
}

device_status() {
  echo '{"cpu_load":"'$(cpu_load)'","used_disk":"'$(used_disk)'","total_disk":"'$(total_disk)'","used_memory":"'$(used_memory)'","total_memory":"'$(total_memory)'"}'
}

# Use for testing or on Mac OS X where top -bn2 is not available
fake_device_status() {
  echo '{"cpu_load":"31.7","used_disk":"3222111","total_disk":"33222111","used_memory":"1024","total_memory":"2048"}'
}

post_status() {
    response=$(post '/api-device/statuses/' "$(device_status)")

    if [ -n "$response" ]; then
        echo "Successfully posted status: $response"
    else
        echo "Error during posting status. Got response: \"$response\""
    fi
}

api_key() {
  cat "$API_KEY_FILE"
}

base_url() {
  cat "$BASE_URL_FILE"
}

set_or_keep() {
  local cache_file="$1"
  local value="$2"

  if [ -n "$value" ]; then
    echo "$value" > "$cache_file"
  fi
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
  # IDEA:
  # waiting loop with timeout to eliminate race condition
  # pkill
  # ev. sleep or wait
  # submit

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
  # source <filename> is not sh compatible => using . <filename> instead
  (trap "finished_command ${command_uuid}" EXIT && . "${command_file}") >${log_file} 2>&1 </dev/null &
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
      check_for_updates
      sleep $SLEEP_PERIOD
  done
}

# Example: script_path => device_daemon.sh
# NOTE: This doesn't work in sourced debug mode
script_name() {
  basename "$0"
}

# Example:
#   add_cronjob "@reboot /root/device_daemon.sh"
# Based on http://stackoverflow.com/a/24892547
add_cronjob() {
  local job="$1"
  (crontab -l ; echo "$job") 2>&1 | grep -v 'no crontab' | sort | uniq | crontab -
}

# Example:
#   remove_cronjob "/root/device_daemon.sh"
remove_cronjob() {
  # Search expression for the cronjob to remove
  local job_search="$1"
  crontab -l 2>&1 | grep -v "no crontab" | grep -v "$job_search" |  sort | uniq | crontab -
}

# NOTE: This doesn't work in sourced debug mode
setup_crontab() {
  if [ "$SETUP_CRONJOB" = 'true' ]; then
    cmd="$(script_path)"
    job="@reboot sleep $SLEEP_ON_STARTUP && $cmd"
    add_cronjob "$job"
  fi
}

check_endpoint_info() {
  if [ -n "$(api_key)" ] && [ -n "$(base_url)" ]; then
    echo "Using api key \"$(api_key)\" against endpoint \"$(base_url)\""
  else
    echo "Endpoint info not complete. \
          Please provide the api key and base url as script arguments \
          and ensure that that script has write permissions within its directory."
    exit 1
  fi
}

# Arguments:
#   api key (mandatory only on first execution; optional to overwrite later)
#   probr base url (mandatory only on first execution; optional to overwrite later)
main() {
  local api_key="$1"
  local base_url="$2"

  save_pid
  set_or_keep $API_KEY_FILE "$api_key"
  set_or_keep $BASE_URL_FILE "$base_url"
  check_endpoint_info
  setup_crontab
  infinite_loop
}
