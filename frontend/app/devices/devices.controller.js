'use strict';

angular.module('probrApp')
    .controller('DevicesCtrl', function ($scope, Device, resourceSocket) {
        Device.query({}, function (devices) {
            $scope.devices = devices;
            resourceSocket.updateResource($scope, devices, 'devices');
        });
    })
    .controller('DeviceStatusCtrl', function ($scope, $stateParams, Status, Device, Command, resourceSocket) {

        var statusLimit = 10;
        var deviceId = $stateParams.id;

        Command.byDevice({deviceId: deviceId}, function (commands) {
            $scope.commands = commands;
            resourceSocket.updateResource($scope, commands, 'commands');
        });

        Device.getStatus({deviceId: deviceId, limit: statusLimit}, function (statuses) {
            $scope.statuses = statuses;
            resourceSocket.updateResource($scope, statuses, 'statuses', 'device', 10);
        });

        Device.get({deviceId: deviceId}, function (device) {
            $scope.device = device;
        });

        $scope.submitCmd = function () {
            $scope.recentCommand = new Command({execute: $scope.cmd, device: $scope.device.uuid});
            $scope.recentCommand.$save(function () {
                console.log("posted cmd");
            });
        }

    });
;
