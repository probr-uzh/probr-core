'use strict';

angular.module('probrApp')
    .directive('deviceCard', function ($filter, $location, Device, resourceSocket) {
        return {
            restrict: 'EA',
            scope: {
                device: '=',
                deleteDevice: '&',
            },
            templateUrl: '/static/app/devices/deviceCard/deviceCard.html',
            link: function (scope, elements, attr) {

                scope.onlineIndicator = function() {
                    if (scope.recentStatus !== undefined) {
                        return "online";
                    }

                    return "offline";
                }

                scope.delete = function () {
                    scope.deleteDevice(scope.device)
                };

                Device.getStatus({deviceId: scope.device.uuid, limit: 10}, function (resultObj) {
                    scope.statuses = resultObj.results;
                    scope.recentStatus = scope.statuses[0];
                    resourceSocket.updateResource(scope, scope.statuses, 'status', 'device', 10);
                });

            }
        }
    });