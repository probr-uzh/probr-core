'use strict';

angular.module('probrApp')
    .factory('Command', function (djResource) {
        var Command = djResource('/api/commands/:commandId/', {commandId: '@id'},
            {
                byDevice: {method: 'GET', url: '/api/devices/:deviceId/commands/', isArray: true}
            }
        );
        return Command;
    });
