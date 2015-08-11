#!/usr/bin/env sh

# Example:
#   abs_path "ubuntu/device_daemon.sh" => "/home/ubuntu/device_daemon.sh"
# Does't support symlinks. Would require a more verbose implementation: http://stackoverflow.com/a/1116890
# Custom implementation of basic `readlink`
abs_path() {
  local rel_path="$1"
  local cwd
  cwd=$(pwd)
  # Issues an error message on some systems although it works as intended
  cd $(dirname "$rel_path") 2>/dev/null
  echo $(pwd)/$(basename "$rel_path")
  cd "$cwd"
}

# Example: script_path => /root/device_daemon.sh
# NOTE: This doesn't work in sourced debug mode
script_path() {
  abs_path "$0"
}

# Example: script_path => /root
# NOTE: This doesn't work in sourced debug mode
basedir() {
  dirname $(script_path)
}

# Imports a script by sourcing it
# NOTE: Some distributions require the full path for sourcing scripts
import() {
  local script="$1"
  . "$(basedir)/${script}"
}

# Setup the PATH might be incorrect if running in a non-interactive shell (e.g., via cronjob)
setup_path() {
  export PATH="$PATH:/sbin:/usr/sbin"
}

# Make the script working from any current working directory
cd "$(basedir)"
import "utils.sh"
setup_path
setup_debug_mode
# Pass original parameters to main function
main "$@"
