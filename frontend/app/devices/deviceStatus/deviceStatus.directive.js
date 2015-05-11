'use strict';

angular.module('probrApp')
    .directive('deviceStatus', function () {
        return {
            restrict: 'EA',
            scope: {
                device: '='
            },
            templateUrl: 'static/app/devices/deviceStatus/deviceStatus.html',
            controller: function ($scope, Device) {
                Device.getStatus({deviceId: $scope.device.uuid}, function (statuses) {
                    $scope.status = statuses[0];
                });
            }
        }
    }).directive("progressBar", ["$timeout", function ($timeout) {
        return {
            restrict: "EA",
            scope: {
                total: '=total',
                complete: '=complete',
                barClass: '@barClass',
                completedClass: '=?'
            },
            transclude: true,
            link: function (scope, elem, attrs) {

                scope.label = attrs.label;
                scope.completeLabel = attrs.completeLabel;
                scope.showPercent = (attrs.showPercent) || false;
                scope.completedClass = (scope.completedClass) || 'progress-bar-danger';

                scope.$watch('complete', function () {

                    //change style at 100%
                    var progress = scope.complete / scope.total;
                    if (progress >= 1) {
                        $(elem).find('.progress-bar').addClass(scope.completedClass);
                    }
                    else if (progress < 1) {
                        $(elem).find('.progress-bar').removeClass(scope.completedClass);
                    }

                });

            },
            template:
            "<div class='progress'>" +
            "   <div class='progress-bar {{barClass}}' title='{{complete/total * 100 | number:0 }}%' style='width:{{complete/total * 100}}%;'>{{showPercent ? (complete/total*100) : complete | number:0}} {{completeLabel}}</div>" +
            "</div>"
        };
    }]);