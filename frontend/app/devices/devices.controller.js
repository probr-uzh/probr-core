'use strict';

angular.module('probrApp')
    .controller('DevicesCtrl', function ($scope, Device) {
        $scope.devices = [];

        var devices = Device.query({}, function () {
            $scope.devices = devices;
        });

    })
    .controller('DeviceStatusCtrl', function ($scope, $stateParams, Device, StatusSocket) {

        $scope.chartOptions = {
            scaleOverride: true,
            scaleSteps: 10,
            scaleStepWidth: 10,
            scaleStartValue: 0,
            maintainAspectRatio: false
        }

        $scope.series = ['CPU-Load'];

        Device.get({deviceId: $stateParams.id}, function (device) {
            $scope.device = device;
            StatusSocket.subscribeForDevice($scope.device.uuid);
            $scope.statuses = StatusSocket.collection;
            $scope.cpuData = StatusSocket.cpuDataCollection;
            $scope.labels = StatusSocket.cpuDataLabels;
        });

    });
;
