'use strict';

angular.module('probrApp')
    .directive('deviceCpuChart', function ($filter, resourceSocket) {
        return {
            restrict: 'EA',
            scope: {
                chart: '=',
                statuses: '=',
                labels: '=',
            },
            templateUrl: '/static/app/devices/deviceCpuChart/deviceCpuChart.html',
            link: function (scope, elements, attr) {

                scope.dataCollections = [[],[]];
                scope.dataLabels = [];

                var pushToUI = function (statusObj) {

                    scope.dataCollections[0].push(statusObj.cpu_load);
                    scope.dataCollections[1].push((statusObj.used_memory / statusObj.total_memory) * 100);

                    scope.dataLabels.push($filter('date')(statusObj.creation_timestamp, 'HH:mm:ss'));

                    if (scope.dataCollections[0].length > 10) {
                        scope.dataCollections[0].shift();
                        scope.dataCollections[1].shift();
                        scope.dataLabels.shift();
                    }

                }

                scope.$watchCollection(
                    "statuses",
                    function (newValue, oldValue) {

                        var diff = _.difference(newValue, oldValue);
                        diff.reverse();

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

                scope.series = ['CPU-Load', 'Memory Usage'];

            }
        }
    });