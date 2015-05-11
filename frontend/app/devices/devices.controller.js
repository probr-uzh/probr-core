'use strict';

angular.module('probrApp')
    .controller('DevicesCtrl', function ($scope, Device) {
        $scope.devices = [];
        var devices = Device.query({}, function () {
            $scope.devices = devices;
        });

    })
    .controller('DeviceStatusCtrl', function ($scope, $stateParams, Device) {
        $scope.device = {};
        $scope.statuses = [];

        $scope.statusChartConfig = {
            options: {
                chart: {
                    type: 'solidgauge'
                },
                pane: {
                    center: ['50%', '85%'],
                    size: '140%',
                    startAngle: -90,
                    endAngle: 90,
                    background: {
                        backgroundColor: '#EEE',
                        innerRadius: '60%',
                        outerRadius: '100%',
                        shape: 'arc'
                    }
                },
                 tooltip: {
                    enabled: false
                }
            },
            title: {
                text: 'CPU Load',
                y: 50
            },
            yAxis: {
                currentMin: 0,
                currentMax: 100,
                title: {
                    y: 140
                },
                stops: [
                    [0.1, '#DF5353'], // red
                    [0.5, '#DDDF0D'], // yellow
                    [0.9, '#55BF3B'] // green
                ],
                lineWidth: 0,
                tickInterval: 20,
                tickPixelInterval: 400,
                tickWidth: 0,
                labels: {
                    y: 15
                }
            },
            loading: false
        }

        var device = Device.get({deviceId: $stateParams.id}, function (device) {
            $scope.device = device;

            Device.getStatus({deviceId: $stateParams.id}, function (statuses) {
                $scope.statuses = statuses;
                $scope.recentStatus = statuses[0];

                $scope.statusChartConfig.series = [{
                    data: [$scope.recentStatus.cpu_load],
                    dataLabels: {
                        borderWidth: 0,
                        format: '<span style="font-size: 20px">{y} %</span>'
                    }
                }];
            });
        });

    });
;
