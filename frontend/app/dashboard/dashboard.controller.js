'use strict';

angular.module('probrApp')
    .controller('DashboardCtrl', function ($scope, Device) {
        $scope.devices = [];
        var devices = Device.query({}, function () {
            $scope.devices = devices.results;
        });

    });
