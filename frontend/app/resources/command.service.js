'use strict';

angular.module('probrApp')
    .factory('Command', function ($resource, $location) {

        var protocol = $location.protocol();
        var host = $location.host();

        var Command = $resource('/api/commands/:commandId/', {commandId: '@uuid'},
            {
                query: {method: 'GET', isArray: false},
                byDevice: {method: 'GET', url: protocol + '://' + host + '/api/commands?device=:deviceId', isArray: false}
            }
        );
        return Command;
    });
