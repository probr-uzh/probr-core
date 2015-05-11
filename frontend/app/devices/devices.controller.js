'use strict';

angular.module('probrApp')
    .controller('DevicesCtrl', function ($scope, Device) {
        $scope.devices = [];

        var devices = Device.query({}, function () {
            $scope.devices = devices;
        });

    })
    .controller('DeviceStatusCtrl', function ($scope, $stateParams, Device, StatusSocket) {

        var device = Device.get({deviceId: $stateParams.id}, function (device) {
            $scope.device = device;
            StatusSocket.subscribeForDevice($scope.device.uuid);
            var statuses = StatusSocket.collection;
        });

    });
;
