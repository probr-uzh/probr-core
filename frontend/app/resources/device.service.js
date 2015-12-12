'use strict';

angular.module('probrApp')
    .factory('Device', function ($resource, $location) {

        var protocol = $location.protocol();
        var host = $location.host();
        var port = $location.port();

        var Device = $resource('/api/devices/:deviceId/', {deviceId: '@uuid'},
            {
                query: {method: 'GET', isArray: false},
                getStatus: {
                    method: 'GET',
                    url: protocol + '://' + host + ':' + port + '/api/statuses?device=:deviceId',
                    isArray: false
                },
                update: { method: 'PUT', isArray: false },
            }
        );
        return Device;
    });
