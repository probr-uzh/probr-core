#!/usr/bin/env bash
VERSION='0.2'
BASE_HOST='probr.sook.ch'
BASE_URL="https://$BASE_HOST"
UUID_FILE='uuid.txt'

# Make the script working location independent
BASEDIR=$(dirname $0)
cd $BASEDIR

abort() {
    echo "$(basename $0) exited with non-zero exit at line $1 status. Exiting ..." >&2
    exit 1
}
trap 'abort $LINENO' 1 2

clean_up() {
    # You might want to do cleanup tasks here
    echo "Exiting ..."
    exit
}
trap 'clean_up' EXIT

# Performs regular expression matching using extended regex (i.e., no escaping required)
# Arguments:
#   string
#   regexp with at least one capture group
# Example:
#   extract '"id":"example_id"' '"id":"([a-zA-Z-_]+)"'
extract() {
	echo $1 | sed -E 's/^.*'$2'.*$/\1/'
}

# Issues an http post request with json payload to the probr server
# Arguments:
#   url
#   json data
# Returns:
#   http response
post() {
    echo $(wget --quiet --output-document=- --header 'Content-Type: application/json' --post-data="$2" -- "$BASE_URL$1")
}

# Issues an http get request to the probr server
# Arguments:
#   url
#   header (e.g. 'Accept: text/plain')
# Returns:
#   http response
get() {
    echo $(wget --quiet --header "$2" --output-document=- -- "$BASE_URL$1")
}

# Read the device uuid from file
device_uuid() {
    cat "$UUID_FILE"
}

# Extract uuid key from json
# Arguments:
#   json string containing a "uuid"
extract_uuid() {
    # UUID regex based on: http://jonalmeida.com/posts/2014/05/20/testing-for-a-correct-uuid/
    local uuid_regex='"uuid":"([0-9a-fA-F]{8}-?[0-9a-fA-F]{4}-?4[0-9a-fA-F]{3}-?[89abAB][0-9a-fA-F]{3}-?[0-9a-fA-F]{12})"'
    extract "$1" "$uuid_regex"
}

register_device() {
    NAME=$(uname -n)    # TODO: hostname is very unlikely a unique device name
    OS=$(uname -a)      # All informations from uname
    TYPE='RPB'          # odroid: armv71, openwrt(vbox): i686, pc/laptop 64 bit: x86_64
    WIFI=''             # TODO: find a way to determine wifi_chip
    DESCRIPTION="Added automatically with device script $VERSION"

    body_data='{"name":"'$NAME'","os":"'$OS'","tags":[],"type":"'$TYPE'","wifi_chip":"'$WIFI'","description":"'$DESCRIPTION'"}'
    response=$(post '/api/devices/' "$body_data")
    local uuid
    uuid=$(extract_uuid "$response")

    if [ $uuid ]; then
        echo "$uuid" > "$UUID_FILE"
        echo "\"$NAME\" successfully registered with device uuid $uuid"
    else
        echo "Error during device registration. Got response: $response"
    fi
}

bootstrap_device() {
    if [ -s "$UUID_FILE" ]; then
        echo "Reusing device uuid $(device_uuid)"
    else
        echo "First time execution, registering device ..."
        register_device
    fi
}

post_status() {
    #total_memory=$(top -bn1 | awk '/KiB Mem/ { print $3 };')
    #used_memory=$(top -bn1 | awk '/KiB Mem/ { print $5 };')
    #total_disk=$(df -k . | awk 'NR==2 { print $4 };')
    #used_disk=$(df -k . | awk 'NR==2 { print $3 };')
    #cpu_load=$(top -bn2 | awk '/Cpu/ { print 100 - $8};' | tail -n1)

    total_memory=100
    used_memory=10
    total_disk=1000
    used_disk=100
    cpu_load=0.1

    body_data='{"device":"'$(device_uuid)'","cpu_load":"'$cpu_load'","used_disk":"'$used_disk'","total_disk":"'$total_disk'","used_memory":"'$used_memory'","total_memory":"'$total_memory'"}'
    response=$(post '/api/statuses/' "$body_data")

    local uuid
    uuid=$(extract_uuid "$response")

    if [ $uuid ]; then
        echo "Successfully posted status with uuid $uuid"
    else
        echo "Error during posting status. Got response $response"
    fi
}

# Strips single ' and double " quoted strings according to http://stackoverflow.com/a/758116
# Example:
#   strip_quotes '"Fo\"od"' => Fo\"od
strip_quotes() {
    echo $1 | sed "s/^\([\"']\)\(.*\)\1\$/\2/g"
}

# Arguments:
#   JSON.sh line string in the tabular separated format: [KEY]    VALUE
# Example:
#   json_data '[0,"execute"] "echo Hello World!"' => echo Hello World!
json_data() {
    echo $(strip_quotes "$(cut -f2 -d$'\t' "$1")")
}

# Arguments:
#   raw json string
#   regex to parse JSON.sh output
# TODO: Debug escaping behavior
# TODO(Joel): Might want to provide a nicer API accepting variable number of arguments
#             such as `parse_json "$raw_json" 0 execute` => [0,\"execute\"]
parse_json() {
    echo $(echo $1 | ./JSON.sh -l | grep --fixed-strings --regexp "$2" | json_data -)
}

# Queries the probr server for non-executed commands
get_commands() {
    echo $(get "/api/devices/$(device_uuid)/commands/")
}

# Arguments:
#   logFilePath
#   commanduuid
submit_result() {
    # We need to make a copy of the log file, since curl can't handle the still opened log file
    cp "$1" "$1.upload"
    echo $(curl -v -F result=@$1.upload $BASE_URL/api/commands/"$2"/)
    rm "$1.upload"
}

# Arguments:
#   commanduuid
#   status (1 = started, 2 = executed)
set_command_status() {
    echo $(post "/api/commands/$1/" "{\"status\":$2}")
}

# Arguments
#   commanduuid
cleanup_command() {
    submit_result "commands/$1.log" $1
    rm commands/$1*
    exit
}

# Arguments:
#   scriptPath
#   logFilePath
#   commandUUID
execute_in_background() {
    (trap "cleanup_command $3" EXIT; source $1) 1>$2 2>&1 &
    echo $!>"commands/$3.pid"
    echo $!
}

execute_commands() {
    mkdir -p commands

    # Get list of all not exucted commands
    commands=$(get "/api/commands/?device=$(device_uuid)&status=0" 'Accept: text/plain')

    # Download the command scripts to ./commands folder in the format UUID.sh
    # and make them executable
    for commanduuid in $commands; do
        echo "Downloading command: $commanduuid"
        wget --quiet --header 'Accept: text/plain' --output-document="./commands/$commanduuid.sh" -- "$BASE_URL/api/commands/$commanduuid"
        chmod +x "./commands/$commanduuid.sh"

        # Set status of command to 'Executing' (1)
        result=$(set_command_status "$commanduuid" 1)

        # Execute script, while piping all output 
        pid=$(execute_in_background "./commands/$commanduuid.sh" "commands/$commanduuid.log" "$commanduuid")

        echo "Started command $commanduuid with pid $pid"

    done
}

main() {
    bootstrap_device

    while :
    do
        echo "Infinite loop [hit CTRL+C to stop]"
        #post_status
        execute_commands
        sleep 5
    done
}

# Pass original parameters to main function
main "$@"
