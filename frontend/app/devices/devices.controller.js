'use strict';

angular.module('probrApp')
    .controller('DevicesCtrl', function ($scope, Device, resourceSocket, $modal) {

        Device.query({}, function (resultObj) {
            $scope.devices = resultObj.results;
            resourceSocket.updateResource($scope, $scope.devices, 'device', 0, true);

            _.forEach($scope.devices, function (device) {
                Device.getStatus({deviceId: device.uuid, limit: 10}, function (resultObj) {
                    device.statuses = resultObj.results;
                    resourceSocket.updateResource($scope, device.statuses, 'status', 10, true, 'device', device.uuid);
                });
            })

            // a new device has been added, attach socket properly
            $scope.$watchCollection('devices', function (newValue, oldValue) {
                var diff = _.difference(newValue, oldValue);
                _.forEach(diff, function (obj) {
                    Device.getStatus({deviceId: obj.uuid, limit: 10}, function (resultObj) {
                        obj.statuses = resultObj.results;
                        resourceSocket.updateResource($scope, obj.statuses, 'status', 10, true, 'device', obj.uuid);
                    });
                });
            });

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

        var timeout;
        $scope.onlineIndicator = function (statuses) {
            var timeoutInterval = 60000;
            if (statuses !== undefined && statuses.length > 0 && new Date(statuses[statuses.length - 1].creation_timestamp) > new Date(new Date().getTime() - timeoutInterval)) {

                var tmpDate = statuses[statuses.length - 1].creation_timestamp;
                clearTimeout(timeout);
                timeout = setTimeout(function () {
                    // haven't gotten new updates in 15 seconds
                    if (tmpDate === statuses[statuses.length - 1].creation_timestamp) {
                        $scope.$apply(function () {
                            statuses[statuses.length - 1].creation_timestamp = new Date(new Date().getTime() - timeoutInterval).toISOString(); // change to force offline status
                        });
                    }
                }, timeoutInterval);

                return "online";
            }

            return "offline";
        }

    })
    .controller('DeviceStatusCtrl', function ($scope, $stateParams, Status, Device, Command, resourceSocket) {

        var statusLimit = 10;
        var deviceId = $stateParams.id;
        $scope.commands = [];

        Command.byDevice({deviceId: deviceId}, function (resultObj) {
            $scope.commands = resultObj.results;
            resourceSocket.updateResource($scope, $scope.commands, 'command', 0, true, 'device', deviceId);
        });

        Device.getStatus({deviceId: deviceId, limit: statusLimit}, function (resultObj) {
            $scope.statuses = resultObj.results;
            resourceSocket.updateResource($scope, $scope.statuses, 'status', statusLimit, true, 'device', deviceId);
        });

        Device.get({deviceId: deviceId}, function (resultObj) {
            $scope.device = resultObj;
        });

        $scope.killCmd = function (uuid) {
            $scope.recentCommand = new Command({execute: "kill $(<commands/"+uuid+".pid)", device: $scope.device.uuid});
            $scope.recentCommand.$save();
        };

        $scope.submitCmd = function () {
            $scope.recentCommand = new Command({execute: $scope.cmd, device: $scope.device.uuid});
            $scope.recentCommand.$save(function (result) {
                $scope.cmd = '';
            });
        };

        var timeout;
        $scope.onlineIndicator = function (statuses) {
            var timeoutInterval = 60000;
            if (statuses !== undefined && statuses.length > 0 && new Date(statuses[statuses.length - 1].creation_timestamp) > new Date(new Date().getTime() - timeoutInterval)) {

                var tmpDate = statuses[statuses.length - 1].creation_timestamp;
                clearTimeout(timeout);
                timeout = setTimeout(function () {
                    // haven't gotten new updates in 15 seconds
                    if (tmpDate === statuses[statuses.length - 1].creation_timestamp) {
                        $scope.$apply(function () {
                            statuses[statuses.length - 1].creation_timestamp = new Date(new Date().getTime() - timeoutInterval).toISOString(); // change to force offline status
                        });
                    }
                }, timeoutInterval);

                return "online";
            }

            return "offline";
        };
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
