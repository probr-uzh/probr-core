'use strict';

angular.module('probrApp')
    .factory('StatusSocket', function ($websocket, $timeout, $location, $filter) {

        var filterString = "";
        var bufferLength = 20;

        var collection = [];
        var cpuDataCollection = [[]];
        var cpuDataLabels = [];

        // Open a WebSocket connection
        var ws = ($location.protocol() == "https" ? "wss" : "ws");
        var dataStream = $websocket(ws + '://' + $location.host() + ':' + $location.port() + '/ws/statuses?subscribe-broadcast');

        dataStream.onOpen(function () {
            console.log("opened connection");
        });

        dataStream.onMessage(function (message) {
            console.log("got message");
            var statusObj = JSON.parse(message.data);
            statusObj.timestamp = message.timeStamp;

            collection.push(statusObj);

            cpuDataCollection[0].push(statusObj.cpu_load);
            cpuDataLabels.push($filter('date')(statusObj.timestamp, 'HH:mm:ss'));

            if (cpuDataCollection[0].length > bufferLength) {
                cpuDataCollection.shift();
                cpuDataLabels.shift();
            }

        }, {filter: filterString});

        return {
            stream: dataStream,
            collection: collection,
            cpuDataLabels: cpuDataLabels,
            cpuDataCollection: cpuDataCollection,
            filterString: filterString,
            bufferSize: bufferLength
        };

    });