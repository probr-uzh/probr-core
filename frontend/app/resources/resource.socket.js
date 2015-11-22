'use strict';

angular.module('probrApp')
    .service('resourceSocket', function ($rootScope, $websocket, $location) {

        var so = this;
        this.watchedResources = [];

        this.updateResource = function ($scope, resource, objectName, bufferSize, updateAndCreate, uuidFilter, uuid) {

            // remove resource object when its scope gets destroyed
            $scope.$on('$destroy', function () {
                so.watchedResources.splice(_.filter(so.watchedResources, {resource: resource}), 1);
            });

            // watch resource
            so.watchedResources.push({
                resource: resource,
                properties: {
                    uuidFilter: { filter: uuidFilter || 'uuid', uuid: uuid },
                    objectName: objectName,
                    bufferSize: bufferSize || 0,
                    updateAndCreate: updateAndCreate || false
                }
            });
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


                var dataObj = JSON.parse(message.data);
                dataObj.timestamp = message.timeStamp;

                var resources = [];
                _.forEach(so.watchedResources, function (resourceObj) {
                    if ((resourceObj.properties.objectName + ':update') === dataObj.object_type) {

                        // check if we have a custom query in place
                        if (resourceObj.properties.uuidFilter.filter !== 'uuid') {

                            if (dataObj.hasOwnProperty([resourceObj.properties.uuidFilter.filter]) && dataObj[resourceObj.properties.uuidFilter.filter] === resourceObj.properties.uuidFilter.uuid) {
                                resources.push(resourceObj);
                            }

                        } else {
                            resources.push(resourceObj);
                        }

                    }
                });

                $rootScope.$apply(function () {
                    _.forEach(resources, function (resourceObj) {

                        // look for objects that can be updated
                        var updateableObjects = _.filter(resourceObj.resource,  {uuid: dataObj.uuid});

                        if (updateableObjects.length > 0) {
                            _.forEach(updateableObjects, function (obj) {
                                _.merge(obj, dataObj);
                            });
                        } else {
                            if (resourceObj.properties.updateAndCreate) {
                                resourceObj.resource.push(dataObj);
                                if (resourceObj.properties.bufferSize > 0 && resourceObj.resource.length > resourceObj.properties.bufferSize) {
                                    resourceObj.resource.shift();
                                }
                            }
                        }

                    });
                });

            });

        }
    });
