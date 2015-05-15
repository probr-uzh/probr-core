'use strict';

angular.module('probrApp')
    .directive('deviceCpuChart', function () {
        return {
            restrict: 'EA',
            scope: {
                chart: '=',
                cpuDataCollection: '=',
                cpuDataLabels: '='
            },
            templateUrl: 'static/app/devices/deviceCpuChart/deviceCpuChart.html',
            link: function (scope, elements, attr) {

                scope.chartOptions = _.assign({
                    scaleOverride: true,
                    scaleSteps: 10,
                    scaleStepWidth: 10,
                    scaleStartValue: 0,
                    maintainAspectRatio: false
                }, scope.chart);

                scope.series = ['CPU-Load'];

            }
        }
    });