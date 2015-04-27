#!/bin/bash
# Script specific vars
VERSION="0.1 beta"


# Device specific vars
NAME=$HOSTNAME
OS=`uname -a`
TYPE="OWR" #find a way to determine type
WIFI="" #find a way to determine wifi_chip
DESCRIPTION="added automatically with device script $VERSION"
BODY_DATA=\{\"name\":\"7$NAME\",\"os\":\"$OS\",\"type\":\"$TYPE\",\"wifi_chip\":\"$WIFI\",\"description\":\"$DESCRIPTION\"\}

# Api specific vars
BASE_URL="http://127.0.0.1:8000"
CONTENT_TYPE="Content-Type: application/json"

response=`wget -qO- --method POST --content-on-error --header "$CONTENT_TYPE" --body-data "$BODY_DATA" $BASE_URL/api/devices/`

UUID_REGEX="\"uuid\":\"([A-Za-z0-9-]+)\""

[[ $response =~ $UUID_REGEX ]]
uuid="${BASH_REMATCH[1]}"

if [ $uuid ]
then
	echo "I managed to register myself, the uuid I received is: $uuid"
else
	echo "there was an issue during registration: $response"
	echo "$uuid">uuid.txt
fi
