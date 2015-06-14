'use strict';

angular.module('probrApp')
    .controller('DevicesCtrl', function ($scope, Device, resourceSocket, $modal) {
        Device.query({}, function (resultObj) {
            $scope.devices = resultObj.results;
            resourceSocket.updateResource($scope, $scope.devices, 'device', 'uuid', 100);

            _.forEach($scope.devices, function (device) {
                Device.getStatus({deviceId: device.uuid, limit: 10}, function (resultObj) {
                    device.statuses = resultObj.results;
                    device.statuses.reverse();
                    resourceSocket.updateResource($scope, device.statuses, 'status', 'device', 10);
                });
            })

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

        $scope.onlineIndicator = function (statuses) {
            if (statuses !== undefined && statuses.length > 0 && new Date(statuses[statuses.length - 1].creation_timestamp) > new Date(new Date().getTime() - 15000)) {

                var tmpDate = statuses[statuses.length - 1].creation_timestamp;
                setTimeout(function () {
                    // haven't gotten new updates in 15 seconds
                    if (tmpDate === statuses[statuses.length - 1].creation_timestamp) {
                        $scope.$apply(function() {
                            statuses[statuses.length - 1].creation_timestamp = new Date(new Date().getTime() - 20000).toISOString(); // change to force offline status
                        });
                    }
                }, 15000);

                return "online";
            }

            return "offline";
        }

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
            $scope.statuses.reverse();
            resourceSocket.updateResource($scope, $scope.statuses, 'status', 'device', 10);
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
