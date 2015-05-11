'use strict';

angular.module('probrApp')
    .factory('StatusSocket', function ($websocket, $timeout, $location, $filter) {

        // Open a WebSocket connection
        var ws = ($location.protocol() == "https" ? "wss" : "ws");
        var dataStream = $websocket(ws + '://' + $location.host() + ':' + $location.port() + '/ws/statuses?subscribe-broadcast');

        dataStream.onOpen(function () {
            console.log("opened connection");
        });

        var collection = [];
        var cpuDataCollection = [[]];
        var cpuDataLabels = [];
        var deviceFilter = [];

        dataStream.onMessage(function (message) {
            console.log("got message");
            var statusObj = JSON.parse(message.data);
            statusObj.timestamp = message.timeStamp;

            if (_.includes(statusObj.device, deviceFilter)) {
                collection.push(statusObj);

                cpuDataCollection[0].push(statusObj.cpu_load);
                cpuDataLabels.push($filter('date')(statusObj.timestamp, 'HH:mm:ss'));

                if (cpuDataCollection[0].length > 10) {
                    cpuDataCollection.shift();
                    cpuDataLabels.shift();
                }

            }

        });

        return {
            collection: collection,
            cpuDataLabels: cpuDataLabels,
            cpuDataCollection: cpuDataCollection,
            subscribeForDevice: function (uuid) {
                deviceFilter.push(uuid);
            }
        };

    });