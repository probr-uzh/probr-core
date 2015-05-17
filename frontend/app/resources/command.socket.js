'use strict';

angular.module('probrApp')
    .factory('CommandSocket', function ($rootScope, $websocket, $timeout, $location) {

        var filterString = "";
        var collection = [];

        // Open a WebSocket connection
        var ws = ($location.protocol() == "https" ? "wss" : "ws");
        var dataStream = $websocket(ws + '://' + $location.host() + ':' + $location.port() + '/ws/commands?subscribe-broadcast');

        dataStream.onOpen(function () {
            console.log("opened connection");
        });

        dataStream.onClose(function () {
            console.log("closed connection");
        });

        dataStream.onMessage(function (message) {

            $rootScope.$apply(function() {
                console.log("new command");
                var commandObj = JSON.parse(message.data);
                collection.push(commandObj);
            });

        }, {filter: filterString});

        return {
            collection: function () {
                return collection;
            },
            setFilter: function (filter) {
                filterString = filter;
            }
        }

    });