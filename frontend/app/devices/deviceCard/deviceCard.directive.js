'use strict';

angular.module('probrApp')
    .directive('deviceCard', function ($filter, $location) {
        return {
            restrict: 'EA',
            scope: {
                device: '=',
            },
            templateUrl: '/static/app/devices/deviceCard/deviceCard.html',
            link: function (scope, elements, attr) {

                scope.goToDevice = function() {
                    $location.path('device/' + scope.device.uuid + '/status');
                }

                /*
                var pushToUI = function (statusObj) {
                    scope.cpuDataCollection[0].push(statusObj.cpu_load);
                    scope.cpuDataLabels.push($filter('date')(statusObj.creation_timestamp, 'HH:mm:ss'));

                    if (scope.cpuDataCollection[0].length > 10) {
                        scope.cpuDataCollection[0].shift();
                        scope.cpuDataLabels.shift();
                    }
                }

                scope.cpuDataCollection = [[]];
                scope.cpuDataLabels = [];

                _.forEach(scope.statuses, function (statusObj) {
                    pushToUI(statusObj);
                });

                scope.$watchCollection(
                    "statuses",
                    function (newValue, oldValue) {

                        var diff = _.difference(newValue, oldValue);

                        _.forEach(diff, function (statusObj) {
                            pushToUI(statusObj);
                        });

                    }
                );

                scope.chartOptions = _.assign({
                    scaleOverride: true,
                    scaleSteps: 10,
                    scaleStepWidth: 10,
                    scaleStartValue: 0,
                    maintainAspectRatio: false,
                    animation: false
                }, scope.chart);

                scope.series = ['CPU-Load'];
                */

            }
        }
    });