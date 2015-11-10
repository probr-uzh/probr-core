'use strict';

angular.module('probrApp')
    .factory('Device', function ($resource, $location) {

        var protocol = $location.protocol();
        var host = $location.host();

        var Device = $resource('/api/devices/:deviceId/', {deviceId: '@uuid'},
            {
                query: {method: 'GET', isArray: false},
                getStatus: {method: 'GET', url: protocol + '://' + host + '/api/statuses?device=:deviceId', isArray: false}
            }
        );
        return Device;
    });
