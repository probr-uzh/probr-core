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
UUID_FILE='uuid.txt'
API_KEY_FILE='api.key'
# BASE_URL='http://localhost:8080'
BASE_URL='https://probr.sook.ch'
# Time to sleep before starting in seconds
# waiting for network/internet to become available
SLEEP_TIME=0

## Debug mode (true|false)
DEBUG=false
AUTO_DETECT_SOURCED=false
TRACE=false
POSIX_COMPATIBLE=false
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


# Performs an http post request with json payload to the probr server
# Arguments:
#   probr url suffix
#   json body data
# Returns:
#   http response
# Example:
#   post '/api/statuses/' '{"cpu_load": "0.4"}'
post() {
    echo $(wget --header 'Content-Type: application/json' \
                --header "Api-Key: $(api_key)" \
                --output-document=- \
                --quiet \
                --post-data="$2" \
                -- "${BASE_URL}$1"
          )
}

api_key() {
  cat "$API_KEY_FILE"
}

# Arguments:
#   $1 api key
set_api_key() {
  echo "$1" > $API_KEY_FILE
}

# Arguments:
#   $1 api key (mandatory only on first execution)
main() {
  sleep $SLEEP_TIME
  API_KEY="$1"
  if [ -n "$API_KEY" ]; then
    set_api_key "$API_KEY"
  fi

  if [ -s "$API_KEY_FILE" ]; then
    echo "Using api key \"$(api_key)\""
  else
    echo "No api key available. Please provide an api key as script argument."
    exit 1
  fi
}


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

# TODO: Remove this debug output after initial script development
echo "FINISH"
