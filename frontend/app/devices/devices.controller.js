'use strict';

angular.module('probrApp')
    .controller('DevicesCtrl', function ($scope, Device) {
        $scope.devices = [];

        var devices = Device.query({}, function () {
            $scope.devices = devices;
        });

    })
    .controller('DeviceStatusCtrl', function ($scope, $stateParams, Device, StatusSocket, Command, CommandSocket) {

        $scope.commandSocket = CommandSocket;

        $scope.submitCmd = function() {
            $scope.recentCommand = new Command({ execute: $scope.cmd, device: $scope.device.uuid });
            $scope.recentCommand.$save(function () {
                console.log("posted cmd");
            });
        }

        Device.get({deviceId: $stateParams.id}, function (device) {
            $scope.device = device;
            $scope.statusSocket = StatusSocket;
            StatusSocket.setFilter($scope.device.uuid);
        });

    });
;
