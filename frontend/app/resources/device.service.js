'use strict';

angular.module('probrApp')
    .factory('Device', function ($resource) {
        var Device = $resource('/api/devices/:deviceId/', {deviceId: '@uuid'},
            {
                query: { method: 'GET', isArray: false },
                getStatus: {method: 'GET', url: '/api/statuses?device=:deviceId', isArray: false }
            }
        );
        return Device;
    });
