'use strict';

angular.module('probrApp')
    .directive('terminal', function () {
        return {
            restrict: 'E',
            scope: {
                devices: '='
            },
            templateUrl: '/static/components/terminal/terminal.html',
            controller: ['$scope', '$filter', 'Device', 'Command', 'CommandTemplate', 'resourceSocket', function ($scope, $filter, Device, Command, CommandTemplate, resourceSocket) {
                var commandLimit = 20;

                $scope.commands = [];
                $scope.commandTemplates = [];
                $scope.commandTemplate = {};

                $scope.getDevice = function (command) {
                    return $filter('filter')($scope.devices, {uuid: command.device})[0];
                };

                $scope.$watchCollection("devices", function () {
                    angular.forEach($scope.devices, function (device) {
                        if (device !== undefined) {
                            Command.byDevice({deviceId: device.uuid}, function (resultObj) {
                                angular.forEach(resultObj.results, function (cmd) {
                                    $scope.commands.push(cmd);
                                });
                                resourceSocket.updateResource($scope, $scope.commands, 'command', commandLimit, true, 'device', device.uuid);
                            });
                        }
                    });
                });

                $scope.killCmd = function (command) {
                    new Command({execute: "kill_command '" + command.uuid + "'", device: $scope.getDevice(command).uuid}).$save();
                };

                $scope.executeCommand = function () {
                    angular.forEach($scope.devices, function (device) {
                        new Command({
                            execute: $scope.commandTemplate.execute,
                            device: device.uuid
                        }).$save(function (result) {
                                $scope.commandTemplate = {};
                            });
                    });
                };

                CommandTemplate.get({}, function (resultObj) {
                    $scope.commandTemplates = resultObj.results;
                });

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
                };

            }]
        };
    });

