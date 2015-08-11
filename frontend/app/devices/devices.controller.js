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


    })
    .controller('DeviceStatusCtrl', function ($scope, $filter, $stateParams,$modal, Status, Device, Command, CommandTemplate, resourceSocket) {

        var commandLimit = 20;
        var statusLimit = 10;
        var deviceId = $stateParams.id;

        $scope.commands = [];
        $scope.commandTemplates = [];
        $scope.commandTemplate = {};

        Command.byDevice({deviceId: deviceId}, function (resultObj) {
            $scope.commands = resultObj.results;
            resourceSocket.updateResource($scope, $scope.commands, 'command', commandLimit, true, 'device', deviceId);
        });

        CommandTemplate.get({}, function (resultObj) {
            $scope.commandTemplates = resultObj.results;
        });

        Device.getStatus({deviceId: deviceId, limit: statusLimit}, function (resultObj) {
            $scope.statuses = resultObj.results;
            resourceSocket.updateResource($scope, $scope.statuses, 'status', statusLimit, true, 'device', deviceId);
        });


        Device.get({deviceId: deviceId}, function (resultObj) {
            $scope.device = resultObj;
        });

        $scope.killCmd = function (uuid) {
            new Command({execute: "kill_command '" + uuid + "'", device: $scope.device.uuid}).$save();
        };

        $scope.executeCommand = function () {
            new Command({execute: $scope.commandTemplate.execute, device: $scope.device.uuid}).$save(function (result) {
                $scope.commandTemplate = {};
            });
        };

        $scope.saveCommandTemplate = function () {
            if (_.has($scope.commandTemplate, 'uuid')) {
                CommandTemplate.update({
                    name: $scope.commandTemplate.name,
                    execute: $scope.commandTemplate.execute,
                    uuid: $scope.commandTemplate.uuid,
                    tags: []
                }, function (resultObj) {
                    $scope.commandTemplate = resultObj;
                });
            } else {
                new CommandTemplate({
                    name: $scope.commandTemplate.name,
                    execute: $scope.commandTemplate.execute,
                    uuid: $scope.commandTemplate.uuid,
                    tags: []
                }).$save(function (resultObj) {
                        $scope.commandTemplate = resultObj;
                        $scope.commandTemplates.push(resultObj);
                    });
            }
        };

        $scope.deleteCommandTemplate = function () {
            CommandTemplate.delete({commandTemplateId: $scope.commandTemplate.uuid}, function (resultObj) {
                $scope.commandTemplates = $filter('filter')($scope.commandTemplates, {uuid: '!' + $scope.commandTemplate.uuid});
                $scope.commandTemplate = {};
            });
        }

        // TODO: This doesn't work as intended, as the ACE-Editor is multi-line and therefore also uses keyUp/keyDown
        /*
        var newestCmd = {};
        var displayedCmd = 0;

        $scope.previousCommand = function () {
            newestCmd = $scope.commandTemplate.execute;
            $scope.commandTemplate.execute = $scope.commands[$scope.commands.length - displayedCmd].execute;

            if ($scope.commands.length - displayedCmd > 0) {
                displayedCmd++;
            }
        }

        $scope.nextCommand = function () {
            if (displayedCmd === 0) {
                $scope.commandTemplate.execute = newestCmd;
            }

            $scope.commandTemplate.execute = $scope.commands[$scope.commands.length - displayedCmd].execute;

            if ($scope.commands.length - displayedCmd !== $scope.commands.length) {
                displayedCmd++;
            }
        }
        */

        $scope.copyCommand = function (){
            var modalInstance = $modal.open({
                animation: true,
                templateUrl: '/static/app/modals/bootstrapCommandModalContent.html',
                controller: 'CopyCommandModalCtrl',
            });

        }

    })
    .controller('DeviceAddCtrl', function ($scope, Device,resourceSocket) {

        $scope.deviceForm = new Device();
        $scope.step = 1;

        $scope.status = "Device not yet bootstrapped."
        var currentURL = window.location.href;
        $scope.hostURL = currentURL.split("/web")[0];
        $scope.statuses = [];

        $scope.createDevice = function (form) {
            $scope.deviceForm.tags = $scope.deviceForm.formTags !== undefined ? $scope.deviceForm.formTags.split(',') : [];
            $scope.deviceForm.$save(function (device) {
                $scope.device = device;
                $scope.step = 2;
                $scope.isLoading = true;

                $scope.deviceURL = $scope.hostURL + '/web/device/' + $scope.device.uuid + '/status';


                $scope.$watch('statuses', function(newVal, oldVal){
                    if(oldVal && newVal){
                        if(oldVal.length < newVal.length){
                            window.location.replace($scope.deviceURL);
                        }
                    }
                },true);

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

        $scope.copyText = function() {
            var range = document.createRange();
            var selection = window.getSelection();

            range.selectNodeContents(document.getElementById('copytext'));
            selection.removeAllRanges();
            selection.addRange(range);

            try{
                var successful = document.execCommand('copy');
                var msg = successful ? 'successful' : 'unsuccessful';
                console.log('Copying text command was ' + msg);
            }catch(err){
                console.log("Failed to copy the text.Copy it by hand.");
            }
        }
    })
    .controller('DeviceDeleteModalCtrl', function ($scope, $modalInstance) {
        $scope.ok = function () {
            $modalInstance.close();
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
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

            try{
                var successful = document.execCommand('copy');
                var msg = successful ? 'successful' : 'unsuccessful';
                console.log('Copying text command was ' + msg);
            }catch(err){
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
