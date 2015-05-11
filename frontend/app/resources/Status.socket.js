'use strict';

angular.module('probrApp')
    .factory('StatusSocket', function ($websocket, $timeout) {

        // Open a WebSocket connection
        var dataStream = $websocket('wss://probr.sook.ch:8000/ws/statuses?subscribe-broadcast');

        dataStream.onOpen(function () {
            console.log("opened connection");
        });

        var collection = [];
        var cpuDataCollection = [[]];
        var cpuDataLabels = [[]];
        var deviceFilter = [];

        dataStream.onMessage(function (message) {
            console.log("got message");
            var statusObj = JSON.parse(message.data);

            statusObj.timestamp = message.timeStamp;

            if (_.includes(statusObj.device, deviceFilter)) {
                collection.push(statusObj);

                cpuDataCollection[0].push(statusObj.cpu_load);

                if (statusObj.timestamp !== undefined && statusObj.timestamp !== null) {
                    cpuDataLabels.push(statusObj.timestamp);
                } else {
                    cpuDataLabels.push(0);
                }

                if (cpuDataCollection.length > 10) {
                    cpuDataCollection.pop();
                    cpuDataLabels.pop();
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