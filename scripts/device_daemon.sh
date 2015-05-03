#!/usr/bin/env bash
VERSION='0.1.0 beta'

UUID_REGEX='"uuid":"([A-Za-z0-9-]+)"'
UUID_FILE='uuid.txt'

BASE_URL='http://127.0.0.1:8000'
CONTENT_TYPE='Content-Type: application/json'

execute() {
    result=$($1 2>&1 </dev/null)
    echo "executed  $1"
    echo "result    $result"
}

# Issues an http post request to the probr server
# Arguments:
#   url
#   json data
# Returns:
#   http response
post() {
    echo $(wget --quiet --output-document=- --header "$CONTENT_TYPE" --post-data="$2" -- "$BASE_URL$1")
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

main() {
    execute 'echo "Hello World!"'

    if [ -a "$UUID_FILE" ]
    then
        echo "you are using: $(device_uuid)"
    else
        echo "first time execution, registering device"
        register_device
    fi

    while :
    do
        echo "infinite loops [ hit CTRL+C to stop]"
        post_status &
        sleep 5
    done
}

main "$@"
