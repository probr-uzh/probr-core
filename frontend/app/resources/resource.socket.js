'use strict';

angular.module('probrApp')
    .service('resourceSocket', function ($rootScope, $websocket, $location) {

        var so = this;
        this.watchedResources = [];

        this.updateResource = function ($scope, resource, objectName, bufferSize, updateAndCreate, uuidFilter, uuid) {

            resource.uuidFilter = {};
            resource.uuidFilter.filter = uuidFilter || 'uuid';
            resource.uuidFilter.uuid = uuid;

            resource.objectName = objectName;
            resource.bufferSize = bufferSize || 0;
            resource.updateAndCreate = updateAndCreate || false;

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
                _.forEach(so.watchedResources, function (resourceObj) {
                    if ((resourceObj.objectName + ':update') === dataObj.object_type) {

                        // check if we have a custom query in place
                        if (resourceObj.uuidFilter.filter !== 'uuid') {
                            if (dataObj.hasOwnProperty([resourceObj.uuidFilter.filter]) && dataObj[resourceObj.uuidFilter.filter] === resourceObj.uuidFilter.uuid) {
                                resources.push(resourceObj);
                            }
                        } else {
                            resources.push(resourceObj);
                        }

                    }
                });

                $rootScope.$apply(function () {
                    _.forEach(resources, function (resourceObj) {

                        // define filterpredict to look for uuid or foreign-key that is a uuid
                        var filterPredicate = {};
                        filterPredicate.uuid = dataObj.uuid;

                        // look for objects that can be updated
                        var updateableObjects = _.filter(resourceObj, filterPredicate);

                        if (updateableObjects.length > 0) {
                            _.forEach(updateableObjects, function (obj) {
                                _.merge(obj, dataObj);
                            });
                        } else {
                            if (resourceObj.updateAndCreate) {
                                resourceObj.push(dataObj);
                                if (resourceObj.bufferSize > 0 && resourceObj.length > resourceObj.bufferSize) {
                                    resourceObj.shift();
                                }
                            }
                        }

                    });
                });

            });

        }
    });
