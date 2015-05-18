'use strict';

angular.module('probrApp')
    .factory('djResourceSocket', function ($rootScope, $websocket, $location) {

        function djResourceSocket(scope) {
            djResourceSocket.filterString = "";
            this.bufferSize = 1000; // high buffersize as default
            var so = this;

            scope.$on('$destroy', function () {
                if (so.dataStream !== undefined) {
                    so.dataStream.close();
                }
            });
        }

        djResourceSocket.prototype.setFilter = function (filterString) {
            this.filterString = filterString;
        }

        djResourceSocket.prototype.setBufferSize = function (bufferSize) {
            this.bufferSize = bufferSize;
        }

        djResourceSocket.prototype.attachToResource = function (djResource, wsEndpoint) {

            var so = this;

            this.resource = djResource;

            // Open a WebSocket connection
            this.ws = ($location.protocol() == "https" ? "wss" : "ws");
            this.dataStream = $websocket(this.ws + '://' + $location.host() + ':' + $location.port() + '/ws/' + wsEndpoint + '?subscribe-broadcast');

            this.dataStream.onOpen(function () {
                console.log("opened connection");
            });

            this.dataStream.onClose(function () {
                console.log("closed connection");
            });

            this.dataStream.onMessage(function (message) {

                var dataObj = JSON.parse(message.data);
                dataObj.timestamp = message.timeStamp;

                _.includes(dataObj, so.filterString)
                {
                    $rootScope.$apply(function () {
                        if (dataObj.uuid !== undefined) {
                            var currentObj = _.find(so.resource, 'uuid', dataObj.uuid)
                            if (currentObj !== undefined) {
                                _.merge(currentObj, dataObj);
                            } else {
                                so.resource.push(dataObj);
                                if (resource.length > so.bufferSize) {
                                    so.resource.shift();
                                }
                            }
                        }
                    });
                }

            });

        }

        return {
            Instance: djResourceSocket
        };

    });
