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

                var resources = [];
                _.forEach(so.watchedResources, function (resource) {
                    if ((resource.objectName + ':update') === dataObj.object_type) {
                        _.forEach(resource, function (res) {
                            if (res.hasOwnProperty(resource.uuidFilter) && res[resource.uuidFilter] == dataObj[resource.uuidFilter]) {
                                resources.push(resource);
                            }
                        });
                    }
                });

                _.forEach(resources, function (resource) {
                    $rootScope.$apply(function () {

                        var currentObj = _.find(resource, function (obj) {
                            if (obj.uuid === dataObj[resource.uuidFilter]) {
                                return true;
                            }
                            return false;
                        });

                        if (currentObj !== undefined) {
                            _.merge(currentObj, dataObj);
                        } else {
                            //if (dataObj[resource.uuidFilter] === resource[0][resource.uuidFilter]) {
                            resource.push(dataObj);
                            if (resource.bufferSize > 0 && resource.length > resource.bufferSize) {
                                resource.shift();
                            }
                            //}
                        }

                    });
                });

            });

        }
    });
