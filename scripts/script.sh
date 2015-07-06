#!/usr/bin/env sh

# This subhell/sourced detection MUST be executed as the very first statement
is_sourced() {
  [ "$_" != "$0" ]
  echo $?
}
SOURCE_DETECTED=$(is_sourced)

#### BEGIN Global variables ####
VERSION='0.3.0'
UUID_FILE='uuid.txt'
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

    if [ "$POSIX_COMPATIBLE" == 'true' ]; then
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


# Performs regular expression matching using extended regex (i.e., no escaping required)
# Arguments:
#   string
#   regexp with at least one capture group
# Returns:
#   first capture group
# Example:
#   extract '"id":"example_id"' '"id":"([a-zA-Z-_]+)"'
#   => example_id
extract() {
  echo $1 | sed -E 's/^.*'$2'.*$/\1/'
}

# Extract uuid key from json
# Arguments:
#   json string containing a "uuid"
extract_uuid() {
    # UUID regex based on: http://jonalmeida.com/posts/2014/05/20/testing-for-a-correct-uuid/
    local uuid_regex='"uuid":"([0-9a-fA-F]{8}-?[0-9a-fA-F]{4}-?4[0-9a-fA-F]{3}-?[89abAB][0-9a-fA-F]{3}-?[0-9a-fA-F]{12})"'
    extract "$1" "$uuid_regex"
}

# Issues an http post request with json payload to the probr server
# Arguments:
#   url
#   json body data
# Returns:
#   http response
# Example:
#   post '/api/devices/' '{"name":"odroid-01"}'
post() {
    echo $(wget --header 'Content-Type: application/json' \
                --output-document=- \
                --quiet \
                --post-data="$2" \
                -- "${BASE_URL}$1"
          )
}

register_device() {
    local name=$(uname -n)
    local os=$(uname -a)
    # TODO: Provide this on manual device registration (via the web interface)
    #  or find a way to automatically determine it
    #  choices: odroid: armv71, openwrt(vbox): i686, pc/laptop 64 bit: x86_64
    # Enum from `probr-core/devices/models.py`
    # RPA := Raspberry Pi Model A
    # RPB := Raspberry Pi Model B
    # ODR := ODROID
    # DWR := DD-WRT Router
    # OWR := OpenWRT Router
    # UKW := Unknown
    local type='ODR'
    # TODO: Find a way to determine the wifi_chip
    #  starting point: dmesg
    local wifi='unknown'
    # [Windows + Mac OS X incompatible]
    local machine
    # machine=$(cat /proc/cpuinfo | awk -F ':' '/machine/ { print $2 }')
    machine='mymac'
    local description="$machine: added with device script $VERSION"

    body_data='{"name":"'$name'","os":"'$os'","tags":[],"type":"'$type'","wifi_chip":"'$wifi'","description":"'$description'"}'
    response=$(post '/api/devices/' "$body_data")
    local uuid
    uuid=$(extract_uuid "$response")

    if [ -n "$uuid" ]; then
        echo "$uuid" > "$UUID_FILE"
        echo "\"$name\" successfully registered with device uuid $uuid"
    else
        echo "Error during device registration. Got response: $response"
    fi
}

# Read the device uuid from file
device_uuid() {
    cat "$UUID_FILE"
}

bootstrap_device() {
    if [ -s "$UUID_FILE" ]; then
        echo "Reusing device uuid $(device_uuid)"
    else
        echo "First time execution, registering device ..."
        register_device
    fi
}

main() {
    sleep $SLEEP_TIME
    bootstrap_device
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
echo "FINISH"
