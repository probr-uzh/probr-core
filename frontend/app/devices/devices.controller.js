'use strict';

angular.module('probrApp')
    .controller('DevicesCtrl', function ($scope, Device) {
        $scope.devices = [];

        var devices = Device.query({}, function () {
            $scope.devices = devices;
        });

    })
    .controller('DeviceStatusCtrl', function ($scope, $stateParams, Device, StatusSocket) {

        $scope.cpuDataCollection = StatusSocket.cpuDataCollection;
        $scope.cpuDataLabels = StatusSocket.cpuDataLabels;

        Device.get({deviceId: $stateParams.id}, function (device) {
            $scope.device = device;
            StatusSocket.filterString = $scope.device.uuid;
        });

    });
;
