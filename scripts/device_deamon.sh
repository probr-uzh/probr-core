#!/bin/bash
# Script specific vars
VERSION="0.1 beta"


UUID_REGEX="\"uuid\":\"([A-Za-z0-9-]+)\""

# Api specific vars
BASE_URL="http://127.0.0.1:8000"
CONTENT_TYPE="Content-Type: application/json"


function registerDevice(){
    # Device specific vars
    NAME=$HOSTNAME
    OS=$(uname -a)
    TYPE="OWR" #find a way to determine type
    WIFI="" #find a way to determine wifi_chip
    DESCRIPTION="added automatically with device script $VERSION"


    body_data=\{\"name\":\"197$NAME\",\"os\":\"$OS\",\"type\":\"$TYPE\",\"wifi_chip\":\"$WIFI\",\"description\":\"$DESCRIPTION\"\}
    response=$(wget -qO- --method POST --content-on-error --header "$CONTENT_TYPE" --body-data "$body_data" $BASE_URL/api/devices/)

    [[ $response =~ $UUID_REGEX ]]
    uuid="${BASH_REMATCH[1]}"

    if [ $uuid ]
    then
        echo "I managed to register myself, the uuid I received is: $uuid"
        echo "$uuid">uuid.txt
    else
        echo "there was an issue during registration: $response"

    fi
}

function remoteExecute(){
    result=$("$1 2>&1")
    echo "executed  $1"
    echo "result    $result"
}

function postStatus(){
    uuid=$(cat uuid.txt)

    total_memory=$(top -bn1 | awk '/KiB Mem/ { print $3 };')
    used_memory=$(top -bn1 | awk '/KiB Mem/ { print $5 };')

    total_disk=$(df -k . | awk 'NR==2 { print $4 };')
    used_disk=$(df -k . | awk 'NR==2 { print $3 };')

    cpu_load=$(top -bn1 | awk '/Cpu/ { print 100 - $8};')

    body_data=\{\"device\":\"$uuid\",\"cpu_load\":\"$cpu_load\",\"used_disk\":\"$used_disk\",\"total_disk\":\"$total_disk\",\"used_memory\":\"$used_memory\",\"total_memory\":\"$total_memory\"\}

    response=$(wget -qO- --method POST --content-on-error --header "$CONTENT_TYPE" --body-data "$body_data" $BASE_URL/api/statuses/)

    [[ $response =~ $UUID_REGEX ]]
    uuid="${BASH_REMATCH[1]}"

    if [ $uuid ]
    then
        echo "I managed to post status, the uuid I received is: $uuid"
    else
        echo "there was an issue during post status: $response"
    fi
}

function main(){
    if [ -a uuid.txt ]
    then
        uuid=$(cat uuid.txt)
        echo "you are using: $uuid"
    else
        echo "first time execution, registering device"
        registerDevice
    fi

    while :
    do
        echo "infinite loops [ hit CTRL+C to stop]"
        postStatus &
        sleep 5
    done
}

remoteExecute 'echo he'
main


