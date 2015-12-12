'use strict';

angular.module('probrApp')
    .controller('DevicesCtrl', function ($scope, Device, Command, resourceSocket, $modal, $filter) {

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


        $scope.executeCommand = function (execute, device) {
            new Command({execute: execute, device: device.uuid}).$save();
        };

        $scope.multiExecuteAction = function () {
            var modalInstance = $modal.open({
                animation: true,
                size: 'lg',
                templateUrl: '/static/app/modals/terminalModalContent.html',
                controller: "TerminalModalCtrl"
            });

            modalInstance.devices = $scope.selectedDevices();
        };

        $scope.updateDeamonAction = function () {
            $scope.performAction(function () {
                var execute = "check_for_updates && update_scripts";
                angular.forEach($scope.selectedDevices(), function (device) {
                    $scope.executeCommand(execute, device);
                });
            });
        };

        $scope.killCommandsAction = function () {
            $scope.performAction(function () {
                var execute = "kill_all_commands";
                angular.forEach($scope.selectedDevices(), function (device) {
                    $scope.executeCommand(execute, device);
                });
            });
        };

        $scope.deleteDevicesAction = function () {
            $scope.performAction(function () {
                angular.forEach($scope.selectedDevices(), function (device) {
                    var deviceResource = new Device(device);
                    deviceResource.$delete(function (resultObj) {
                        $scope.devices.splice($scope.devices.indexOf(device), 1);
                    });
                });
            });
        };

        $scope.selectedDevices = function () {
            return $filter('filter')($scope.devices, {isSelected: true});
        };

        $scope.deleteDevice = function (device) {
            var modalInstance = $modal.open({
                animation: true,
                templateUrl: '/static/app/modals/confirmationModalContent.html',
                controller: 'ConfirmationModalCtrl',
            });

            modalInstance.result.then(function () {
                var deviceResource = new Device(device);
                deviceResource.$delete(function (resultObj) {
                    $scope.devices.splice($scope.devices.indexOf(device), 1);
                });
            }, function () {

            });
        };

        $scope.performAction = function (actionCB) {
            var modalInstance = $modal.open({
                animation: true,
                templateUrl: '/static/app/modals/confirmationModalContent.html',
                controller: 'ConfirmationModalCtrl',
            });

            modalInstance.result.then(actionCB, function () {

            });
        };

    })
    .controller('DeviceStatusCtrl', function ($scope, $filter, $stateParams, $modal, Status, Device, Command, CommandTemplate, resourceSocket) {
        var statusLimit = 10;
        var deviceId = $stateParams.id;

        Device.getStatus({deviceId: deviceId, limit: statusLimit}, function (resultObj) {
            $scope.statuses = resultObj.results;
            resourceSocket.updateResource($scope, $scope.statuses, 'status', statusLimit, true, 'device', deviceId);
        });

        Device.get({deviceId: deviceId}, function (resultObj) {
            $scope.device = resultObj;
        });

        $scope.editDevice = function () {
            var modalInstance = $modal.open({
                animation: true,
                templateUrl: '/static/app/modals/deviceEditModalContent.html',
                controller: 'DeviceEditModalCtrl',
                resolve: {
                    device: function () {
                        return $scope.device;
                    }
                }
            });
        };

        $scope.executeCommand = function (execute) {
            new Command({execute: execute, device: $scope.device.uuid}).$save();
        };

        $scope.updateDeamonAction = function () {
            $scope.executeCommand("check_for_updates && update_scripts");
        };

        $scope.killCommandsAction = function () {
            $scope.executeCommand("kill_all_commands");
        };

    })
    .controller('DeviceAddCtrl', function ($scope, Device, resourceSocket) {

        $scope.deviceForm = new Device();
        $scope.step = 1;

        $scope.status = "Device not yet bootstrapped."
        var currentURL = window.location.href;
        $scope.hostURL = currentURL.split("/web")[0];
        $scope.statuses = [];

        $scope.saveDevice = function (form) {
            $scope.deviceForm.tags = $scope.deviceForm.formTags !== undefined ? $scope.deviceForm.formTags.split(',') : [];
            $scope.deviceForm.$save(function (device) {
                $scope.device = device;
                $scope.step = 2;
                $scope.isLoading = true;

                $scope.deviceURL = $scope.hostURL + '/web/device/' + $scope.device.uuid + '/status';


                $scope.$watch('statuses', function (newVal, oldVal) {
                    if (oldVal && newVal) {
                        if (oldVal.length < newVal.length) {
                            window.location.replace($scope.deviceURL);
                        }
                    }
                }, true);

                Device.getStatus({deviceId: $scope.device.uuid, limit: 50}, function (resultObj) {
                    $scope.statuses = resultObj.results;
                    resourceSocket.updateResource($scope, $scope.statuses, 'status', 50, true, 'device', $scope.device.uuid);
                });

            }, function (err) {
                $scope.errors = {};

                // Update validity of form fields that match the django errors
                angular.forEach(err.data, function (error, field) {
                    form[field].$setValidity('django', false);
                    $scope.errors[field] = error;
                });
            });
        };

        $scope.bootstrap = function () {
            $scope.step = 3;
            console.log('Bootstrapped the device succesfully.');
        };

        $scope.copyText = function () {
            var range = document.createRange();
            var selection = window.getSelection();

            range.selectNodeContents(document.getElementById('copytext'));
            selection.removeAllRanges();
            selection.addRange(range);

            try {
                var successful = document.execCommand('copy');
                var msg = successful ? 'successful' : 'unsuccessful';
                console.log('Copying text command was ' + msg);
            } catch (err) {
                console.log("Failed to copy the text.Copy it by hand.");
            }
        }
    })
    .controller('ConfirmationModalCtrl', function ($scope, $modalInstance) {
        $scope.ok = function () {
            $modalInstance.close();
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    })
    .controller('TerminalModalCtrl', function ($scope, $modalInstance) {
        $scope.devices = $modalInstance.devices;
        $scope.close = function () {
            $modalInstance.close();
        };
    })
    .controller('DeviceEditModalCtrl', function ($scope, $modalInstance, device) {
        $scope.deviceForm = device;
        $scope.deviceForm.formTags = $scope.deviceForm.tags.join();
        $scope.saveDevice = function (form) {
            $scope.deviceForm.tags = $scope.deviceForm.formTags !== undefined ? $scope.deviceForm.formTags.split(',') : [];
            console.log($scope.deviceForm.tags);
            $scope.deviceForm.$update(function (device) {
                $modalInstance.close();
            }, function (err) {
                $scope.errors = {};

                // Update validity of form fields that match the django errors
                angular.forEach(err.data, function (error, field) {
                    form[field].$setValidity('django', false);
                    $scope.errors[field] = error;
                });
            });
        };
    })
    .controller('CopyCommandModalCtrl', function ($scope, $modalInstance, $stateParams, Device) {


        var deviceId = $stateParams.id;
        Device.get({deviceId: deviceId}, function (resultObj) {
            $scope.device = resultObj;
            console.log(JSON.stringify($scope.device));
            var currentURL = window.location.href;
            var hostURL = currentURL.split("/web")[0];
            $scope.bootstrapCommand = "wget -qO- " + hostURL + "/static/bootstrap.sh | sh -s " + $scope.device.apikey + " " + hostURL;
        });


        $scope.copy = function () {
            console.log("copy");
            var range = document.createRange();
            var selection = window.getSelection();

            range.selectNodeContents(document.getElementById('copytext'));
            selection.removeAllRanges();
            selection.addRange(range);

            try {
                var successful = document.execCommand('copy');
                var msg = successful ? 'successful' : 'unsuccessful';
                console.log('Copying text command was ' + msg);
            } catch (err) {
                console.log("Failed to copy the text.Copy it by hand.");
            }
            $modalInstance.close();
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    });
;
;
