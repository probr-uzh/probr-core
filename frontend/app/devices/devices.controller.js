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

        var device = Device.get({ deviceId: $stateParams.id }, function (device) {
            $scope.device = device;

            Device.getStatus({ deviceId: $stateParams.id }, function (statuses) {
                $scope.statuses = statuses;
            });

        });

    });
;
