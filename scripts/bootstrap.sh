#!/usr/bin/env sh

API_KEY="$1"
BASE_URL="$2"
PROBR_DIR=probr

update_script() {
  local base_url="$1"
  local script="$2"
  wget --quiet --output-document="${PROBR_DIR}/${script}" -- "${base_url}/static/${script}"
}

mkdir -p "$PROBR_DIR"
update_script "$BASE_URL" "utils.sh"
update_script "$BASE_URL" "device_daemon.sh"

chmod +x "${PROBR_DIR}/device_daemon.sh"
"./${PROBR_DIR}/device_daemon.sh" "$API_KEY" "$BASE_URL" # >/dev/null 2>&1 </dev/null &
# echo "Started device daemon with pid $!"