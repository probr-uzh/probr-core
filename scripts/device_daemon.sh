#!/usr/bin/env bash
VERSION='0.1.0 beta'
# DEPENDENCIES
# ./JSON.sh (https://github.com/dominictarr/JSON.sh) must be executable

abort() {
    # Do cleanup tasks here
    echo "$(basename $0) exited with non-zero exit status. Exiting ..." >&2
    exit 1
}
trap 'abort' ERR

UUID_REGEX='"uuid":"([A-Za-z0-9-]+)"'
UUID_FILE='uuid.txt'

BASE_URL='http://127.0.0.1:8000'
CONTENT_TYPE='Content-Type: application/json'

execute() {
    result=$($1 2>&1 </dev/null)
    echo "executed  $1"
    echo "result    $result"
}

# Issues an http post request with json payload to the probr server
# Arguments:
#   url
#   json data
# Returns:
#   http response
post() {
    echo $(wget --quiet --output-document=- --header "$CONTENT_TYPE" --post-data="$2" -- "$BASE_URL$1")
}

# Issues an http get request to the probr server
# Arguments:
#   url
# Returns:
#   http response
get() {
    echo $(wget --quiet --output-document=- -- "$BASE_URL$1")
}

device_uuid() {
    echo $(cat "$UUID_FILE")
}

register_device() {
    NAME=$HOSTNAME
    OS=$(uname -a)
    TYPE='RPB'  # TODO: find a way to determine type
    WIFI=''     # TODO: find a way to determine wifi_chip
    DESCRIPTION="Added automatically with device script $VERSION"

    body_data='{"name":"'197$NAME'","os":"'$OS'","type":"'$TYPE'","wifi_chip":"'$WIFI'","description":"'$DESCRIPTION'"}'
    response=$(post '/api/devices/' "$body_data")

    [[ $response =~ $UUID_REGEX ]]
    uuid="${BASH_REMATCH[1]}"

    echo "uuid=$uuid"

    if [ $uuid ]
    then
        echo "I managed to register myself, the uuid I received is: $uuid"
        echo "$uuid" > "$UUID_FILE"
    else
        echo "there was an issue during registration: $response"
    fi
}

bootstrap_device() {
    if [ -a "$UUID_REGEXID_FILE" ]
    then
        echo "you are using: $(device_uuid)"
    else
        echo "first time execution, registering device"
        register_device
    fi
}

post_status() {
    uuid=$(device_uuid)

    total_memory=$(top -bn1 | awk '/KiB Mem/ { print $3 };')
    used_memory=$(top -bn1 | awk '/KiB Mem/ { print $5 };')

    total_disk=$(df -k . | awk 'NR==2 { print $4 };')
    used_disk=$(df -k . | awk 'NR==2 { print $3 };')

    cpu_load=$(top -bn1 | awk '/Cpu/ { print 100 - $8};')

    body_data='{"device":"'$uuid'","cpu_load":"'$cpu_load'","used_disk":"'$used_disk'","total_disk":"'$total_disk'","used_memory":"'$used_memory'","total_memory":"'$total_memory'"}'
    response=$(post '/api/statuses/' "$body_data")

    [[ $response =~ $UUID_REGEX ]]
    uuid="${BASH_REMATCH[1]}"

    if [ $uuid ]
    then
        echo "I managed to post status, the uuid I received is: $uuid"
    else
        echo "there was an issue during post status: $response"
    fi
}

# Queries the probr server for non-executed commands
get_commands() {
    echo $(get "/api/commands/$(device_uuid)/")
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
    cut -f2 -d$'\t' "$1"
}

# Arguments:
#   raw json string
#   regex to parse JSON.sh output
parse_json() {
    echo $1 | ./JSON.sh -l | grep --fixed-strings --regexp "$2" | json_data -
}

# parse_commands() {

# }

execute_remote_commands() {
    local command
    command=$(parse_json "$(get_commands)" "[0,\"execute\"]")
    execute "$command"
}

main() {
    bootstrap_device
    execute 'echo "Hello World!"'
    execute_remote_commands

    while :
    do
        echo "infinite loop [ hit CTRL+C to stop]"
        post_status
        sleep 5
    done
}

execute_remote_commands

# Pass original parameters to main function
# main "$@"
