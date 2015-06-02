'use strict';

angular.module('probrApp')
    .factory('Command', function ($resource) {
        var Command = $resource('/api/commands/:commandId/', { commandId: '@uuid' },
            {
                query: { method: 'GET', isArray: false },
                byDevice: {method: 'GET', url: '/api/devices/:deviceId/commands/', isArray: false }
            }
        );
        return Command;
    });
