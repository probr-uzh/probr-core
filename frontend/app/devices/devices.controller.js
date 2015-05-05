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

        var device = Device.find({ deviceId: $stateParams.id }, function () {
            $scope.device = device;
        });

    });
;
