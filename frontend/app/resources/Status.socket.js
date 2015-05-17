'use strict';

angular.module('probrApp')
    .factory('StatusSocket', function ($rootScope, $websocket, $timeout, $location, $filter) {

        var filterString = "";
        var bufferLength = 10;

        var collection = [];
        var cpuDataCollection = [[]];
        var cpuDataLabels = [];

        // Open a WebSocket connection
        var ws = ($location.protocol() == "https" ? "wss" : "ws");
        var dataStream = $websocket(ws + '://' + $location.host() + ':' + $location.port() + '/ws/statuses?subscribe-broadcast');

        dataStream.onOpen(function () {
            console.log("opened connection");
        });

        dataStream.onClose(function () {
            console.log("closed connection");
        });

        dataStream.onMessage(function (message) {

            $rootScope.$apply(function() {
                console.log("new status");
                var statusObj = JSON.parse(message.data);
                statusObj.timestamp = message.timeStamp;

                collection.push(statusObj);

                cpuDataCollection[0].push(statusObj.cpu_load);
                cpuDataLabels.push($filter('date')(statusObj.timestamp, 'HH:mm:ss'));

                if (cpuDataCollection[0].length > bufferLength) {
                    cpuDataCollection[0].shift();
                    cpuDataLabels.shift();
                }
            });

        }, {filter: filterString});

        return {
            collection: function () {
                return collection;
            },
            cpuDataLabels: function () {
                return cpuDataLabels;
            },
            cpuDataCollection: function () {
                return cpuDataCollection;
            },
            setFilter: function (filter) {
                filterString = filter;
            }
        }

    });