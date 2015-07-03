'use strict';

angular.module('probrApp')
    .directive('statusIndicator', function () {
        return {
            restrict: 'EA',
            scope: {
                statuses: '=',
                device: '=',
            },
            templateUrl: '/static/app/devices/statusIndicator/statusIndicator.html',
            link: function (scope, elements, attr) {

                var timeout;

                scope.onlineIndicator = function (statuses) {
                    var timeoutInterval = 60000;
                    if (statuses !== undefined && statuses.length > 0 && new Date(statuses[statuses.length - 1].creation_timestamp) > new Date(new Date().getTime() - timeoutInterval)) {

                        var tmpDate = statuses[statuses.length - 1].creation_timestamp;
                        clearTimeout(timeout);

                        timeout = setTimeout(function () {
                            // haven't gotten new updates in 15 seconds
                            if (tmpDate === statuses[statuses.length - 1].creation_timestamp) {
                                scope.$apply(function () {
                                    statuses[statuses.length - 1].creation_timestamp = new Date(new Date().getTime() - timeoutInterval).toISOString(); // change to force offline status
                                });
                            }
                        }, timeoutInterval);

                        return "online";
                    }

                    return "offline";
                }

            }
        }
    });