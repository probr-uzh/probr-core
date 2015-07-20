'use strict';

angular.module('probrApp')
    .config(function ($stateProvider) {
        $stateProvider
            .state('devices', {
                url: '/devices',
                templateUrl: '/static/app/devices/devices.html',
                controller: 'DevicesCtrl'
            })
            .state('deviceStatus', {
                url: '/device/:id/status',
                templateUrl: '/static/app/devices/deviceStatus.html',
                controller: 'DeviceStatusCtrl'
            })
            .state('deviceAdd', {
                url: '/device/add',
                templateUrl: '/static/app/devices/deviceAdd.html',
                controller: 'DeviceAddCtrl'
            });
        ;
    });