'use strict';

angular.module('probrApp')
    .controller('DevicesCtrl', function ($scope, Device, resourceSocket, $modal, $templateCache) {
        Device.query({}, function (resultObj) {
            $scope.devices = resultObj.results;
            resourceSocket.updateResource($scope, $scope.devices, 'devices');
        });

        $scope.deleteDevice = function (device) {
            var modalInstance = $modal.open({
                animation: true,
                templateUrl: '/static/app/modals/deleteModalContent.html',
                controller: 'DeviceDeleteModalCtrl',
            });

            modalInstance.result.then(function () {
                var deviceResource = new Device(device);
                deviceResource.$delete(function (resultObj) {
                    $scope.devices.splice($scope.devices.indexOf(device), 1);
                });
            }, function () {

            });
        };
    })
    .controller('DeviceStatusCtrl', function ($scope, $stateParams, Status, Device, Command, resourceSocket) {

        var statusLimit = 10;
        var deviceId = $stateParams.id;

        Command.byDevice({deviceId: deviceId}, function (resultObj) {
            $scope.commands = resultObj.results;
            resourceSocket.updateResource($scope, $scope.commands, 'command', 'device');
        });

        Device.getStatus({deviceId: deviceId, limit: statusLimit}, function (resultObj) {
            $scope.statuses = resultObj.results;
            resourceSocket.updateResource($scope, $scope.statuses, 'statuses', 'device', 10);
        });

        Device.get({deviceId: deviceId}, function (resultObj) {
            $scope.device = resultObj;
        });

        $scope.submitCmd = function () {
            $scope.recentCommand = new Command({execute: $scope.cmd, device: $scope.device.uuid});
            $scope.recentCommand.$save(function () {
                $scope.cmd = '';
            });
        }

    })

    .controller('DeviceDeleteModalCtrl', function ($scope, $modalInstance) {
        $scope.ok = function () {
            $modalInstance.close();
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    });
;
;
