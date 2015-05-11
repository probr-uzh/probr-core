'use strict';

angular.module('probrApp')
    .directive('deviceStatus', function () {
        return {
            restrict: 'EA',
            scope: {
                device: '='
            },
            templateUrl: 'static/app/devices/deviceStatus/deviceStatus.html',
            controller: function ($scope, Device, StatusSocket) {
                Device.getStatus({deviceId: $scope.device.uuid}, function (statuses) {
                    $scope.status = statuses[0];
                });
            }
        }
    });