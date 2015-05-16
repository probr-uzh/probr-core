#!/usr/bin/env ash
VERSION='0.1.1 beta'
# DEPENDENCIES
# ./JSON.sh from https://github.com/dominictarr/JSON.sh must be executable

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


BASE_HOST='probr.sook.ch'
BASE_URL="https://$BASE_HOST"

CONTENT_TYPE='Content-Type: application/json'
UUID_FILE='uuid.txt'

install_dependencies() {
    if [[ ! -a JSON.sh ]]; then
        wget 'https://raw.githubusercontent.com/dominictarr/JSON.sh/master/JSON.sh'
        chmod +x JSON.sh
    fi
}

# Execute an arbitrary bash command and return stdout and stderr
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
    if [ -n $(wget --help|grep post-data) ]; then
        local CONTENT_LEN=$(echo  $2 | wc -c)
        local raw_payload="POST $1 HTTP/1.0\r\nHost: $BASE_HOST\r\n$CONTENT_TYPE\r\nContent-Length: $CONTENT_LEN\r\n\r\n$2"
        echo $( (echo $raw_payload && sleep 5) | openssl s_client -connect $BASE_HOST:443 2>&1 )
    else

        echo $(wget --no-check-certificate --quiet --output-document=- --header "$CONTENT_TYPE" --post-data="$2" -- "$BASE_URL$1")
    fi
}

# Issues an http get request to the probr server
# Arguments:
#   url
# Returns:
#   http response
get() {
    echo $(wget --no-check-certificate --quiet --output-document=- -- "$BASE_URL$1")
}

# Read the device uuid from file
device_uuid() {
    cat "$UUID_FILE"
}

# Extract uuid key from json
# Arguments:
#   json string
extract_uuid() {
    echo $1 | grep -o "\"[A-Za-z0-9-]\{36\}\"" | grep -o "[A-Za-z0-9-]\{36\}"
}


register_device() {
    NAME=$HOSTNAME # TODO: hostname is very unlikely a unique device name
    OS=$(uname -a)
    TYPE='RPB'  # TODO: find a way to determine type
    WIFI=''     # TODO: find a way to determine wifi_chip
    DESCRIPTION="Added automatically with device script $VERSION"

    body_data='{"name":"'$NAME'","os":"'$OS'","tags":[],"type":"'$TYPE'","wifi_chip":"'$WIFI'","description":"'$DESCRIPTION'"}'
    response=$(post '/api/devices/' "$body_data")
    local uuid
    uuid=$(extract_uuid "$response")

    if [ $uuid ]; then
        echo "I managed to register myself, the uuid I received is: $uuid"
        echo "$uuid" > "$UUID_FILE"
    else
        echo "there was an issue during registration: $response"
    fi
}

bootstrap_device() {
    if [[ -s "$UUID_FILE" ]]; then
        echo "you are using: $(device_uuid)"
    else
        echo "first time execution, registering device"
        register_device
    fi
}

post_status() {
    total_memory=$(top -bn1 | awk '/KiB Mem/ { print $3 };')
    used_memory=$(top -bn1 | awk '/KiB Mem/ { print $5 };')

    total_disk=$(df -k . | awk 'NR==2 { print $4 };')
    used_disk=$(df -k . | awk 'NR==2 { print $3 };')

    cpu_load=$(top -bn2 | awk '/Cpu/ { print 100 - $8};' | tail -n1)

    body_data='{"device":"'$(device_uuid)'","cpu_load":"'$cpu_load'","used_disk":"'$used_disk'","total_disk":"'$total_disk'","used_memory":"'$used_memory'","total_memory":"'$total_memory'"}'
    response=$(post '/api/statuses/' "$body_data")

    local uuid
    uuid=$(extract_uuid "$response")
    echo $uuid

    if [[ $uuid ]]; then
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
    echo $(strip_quotes "$(cut -f2 -d$'\t' "$1")")
}

# Arguments:
#   raw json string
#   regex to parse JSON.sh output
# TODO(Joel): Might want to provide a nicer API accepting variable number of arguments
#             such as `parse_json "$raw_json" 0 execute` => [0,\"execute\"]
parse_json() {
    echo $(echo $1 | ./JSON.sh -l | grep -e "$2" | json_data -)
}

execute_remote_commands() {
    local command
    command=$(parse_json "$(get_commands)" "[0,\"execute\"]")
    execute "$command"
}

main() {
    install_dependencies
    bootstrap_device
    execute_remote_commands

    while :
    do
        echo "infinite loop [ hit CTRL+C to stop]"
        post_status
        sleep 5
    done
}

# Pass original parameters to main function
main "$@"
