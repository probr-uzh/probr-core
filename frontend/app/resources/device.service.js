'use strict';

angular.module('probrApp')
    .factory('Device', function ($resource) {
        var Device = $resource('/api/devices/:deviceId/', {deviceId: '@uuid'},
            {
                query: { method: 'GET', isArray: false },
                getStatus: {method: 'GET', url: '/api/devices/:deviceId/statuses/', isArray: false }
            }
        );
        return Device;
    });
