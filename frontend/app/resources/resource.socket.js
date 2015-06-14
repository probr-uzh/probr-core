'use strict';

angular.module('probrApp')
    .service('resourceSocket', function ($rootScope, $websocket, $location) {

        var so = this;
        this.watchedResources = [];

        this.updateResource = function ($scope, resource, objectName, uuidFilter, bufferSize) {
            resource.uuidFilter = uuidFilter || 'uuid';
            resource.objectName = objectName;
            resource.bufferSize = bufferSize || 0;

            // remove resource object when its scope gets destroyed
            $scope.$on('$destroy', function () {
                so.watchedResources.splice(so.watchedResources.indexOf(resource), 1);
            });

            // watch resource
            so.watchedResources.push(resource);
        }

        this.disconnect = function () {
            if (so.socket) {
                so.socket.close();
            }
        }

        this.connect = function (endPoint) {

            // TODO: connect to user endpoint
            // Open a WebSocket connection
            so.wsProtocol = ($location.protocol() == "https" ? "wss" : "ws");
            so.socket = $websocket(so.wsProtocol + '://' + $location.host() + ':' + $location.port() + '/ws/socket?subscribe-broadcast&publish-broadcast');

            so.socket.onOpen(function () {
                console.log("opened connection");
            });

            so.socket.onClose(function () {
                console.log("closed connection");
            });

            so.socket.onError(function (error) {
                console.log(error);
            });

            so.socket.onMessage(function (message) {

                console.log(message);

                var dataObj = JSON.parse(message.data);
                dataObj.timestamp = message.timeStamp;

                var resource = _.find(so.watchedResources, function (obj) {
                    if ((obj.objectName + ':update') == dataObj.type) {
                        return true;
                    }

                    return false;
                });

                if (resource && dataObj[resource.uuidFilter] !== null) {
                    $rootScope.$apply(function () {
                        if (dataObj.uuid !== undefined) {
                            var currentObj = _.find(resource, 'uuid', dataObj.uuid)
                            if (currentObj !== undefined) {
                                _.merge(currentObj, dataObj);
                            } else {
                                resource.push(dataObj);
                                if (resource.bufferSize > 0 && resource.length > resource.bufferSize) {
                                    resource.shift();
                                }
                            }
                        }
                    });
                }

            });

        }
    });
