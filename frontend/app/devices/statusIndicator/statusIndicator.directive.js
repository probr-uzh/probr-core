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

                scope.onlineIndicator = function () {
                    var timeoutInterval = 15000;


                    if (scope.statuses !== undefined && scope.statuses.length > 0) {
                        var timeDifference = new Date().getTime() - new Date(scope.statuses[scope.statuses.length - 1].creation_timestamp);
                        //console.log(timeDifference);

                        if (timeDifference<timeoutInterval) {
                            var tmpDate = scope.statuses[scope.statuses.length - 1].creation_timestamp;
                            clearTimeout(timeout);

                            timeout = setTimeout(function () {
                                // haven't gotten new updates in 15 seconds
                                if (tmpDate === scope.statuses[scope.statuses.length - 1].creation_timestamp) {
                                    scope.$apply(function () {
                                        scope.statuses[scope.statuses.length - 1].creation_timestamp = new Date(new Date().getTime() - timeoutInterval).toISOString(); // change to force offline status
                                    });
                                }
                            }, timeoutInterval);

                            return "online";
                        } else {

                            return "offline";
                        }
                    }

                };
            }
    };
});