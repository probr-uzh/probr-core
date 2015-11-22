'use strict';

angular.module('probrApp')
    .factory('Command', function ($resource, $location) {

        var protocol = $location.protocol();
        var host = $location.host();
        var port = $location.port();

        var Command = $resource('/api/commands/:commandId/', {commandId: '@uuid'},
            {
                query: {method: 'GET', isArray: false},
                byDevice: {method: 'GET', url: protocol + '://' + host + ':' + port + '/api/commands?device=:deviceId', isArray: false}
            }
        );
        return Command;
    });
