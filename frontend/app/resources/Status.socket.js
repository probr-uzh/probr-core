'use strict';

angular.module('probrApp')
    .factory('StatusSocket', function ($websocket) {

        // Open a WebSocket connection
        var dataStream = $websocket('ws://localhost/statuses');
        var collection = [];
        var deviceFilter = [];

        dataStream.onMessage(function (message) {
            var statusObj = JSON.parse(message.data);
            statusObj.timestamp = message.timeStamp;
            if (_.includes(statusObj.device, deviceFilter)) {
                collection.push(statusObj);
            }
        });

        return {
            collection: collection,
            subscribeForDevice: function (uuid) {
                deviceFilter.push(uuid);
            }
        };

    });