'use strict';

angular.module('probrApp')
    .directive('deviceCpuChart', function ($filter) {
        return {
            restrict: 'EA',
            scope: {
                chart: '=',
                statuses: '=',
                labels: '=',
            },
            templateUrl: '/static/app/devices/deviceCpuChart/deviceCpuChart.html',
            link: function (scope, elements, attr) {

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
                    scaleSteps: 5,
                    scaleStepWidth: 20,
                    scaleStartValue: 0,
                    maintainAspectRatio: false,
                    animation: false
                }, scope.chart);

                if (scope.labels == false) {
                    scope.chartOptions.showScale = false;
                    scope.chartOptions.scaleShowLabels = false;
                    scope.chartOptions.showTooltips = false;
                    scope.chartOptions.pointDot = false;
                }

                scope.series = ['CPU-Load'];


            }
        }
    });