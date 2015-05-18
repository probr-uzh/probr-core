'use strict';

angular.module('probrApp')
    .controller('DevicesCtrl', function ($scope, Device, djResourceSocket) {
        Device.query({}, function (devices) {
            var deviceSocket = new djResourceSocket.Instance($scope);
            deviceSocket.attachToResource(devices, "devices");
            $scope.devices = devices;
        });
    })
    .controller('DeviceStatusCtrl', function ($scope, $stateParams, Status, Device, Command, djResourceSocket) {

        var statusLimit = 10;
        var deviceId = $stateParams.id;

        Command.byDevice({deviceId: deviceId}, function (commands) {
             var commandSocket = new djResourceSocket.Instance($scope);
            commandSocket.attachToResource(commands, "commands");
            commandSocket.setFilter(deviceId);
            $scope.commands = commands;
        });

        Device.getStatus({deviceId: deviceId, limit: statusLimit}, function (statuses) {
            var statusSocket = new djResourceSocket.Instance($scope);
            statusSocket.attachToResource(statuses, "statuses");
            statusSocket.setFilter(deviceId);
            statusSocket.setBufferSize(statusLimit);
            $scope.statuses = statuses;
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
