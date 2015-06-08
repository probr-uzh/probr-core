'use strict';

angular.module('probrApp')
    .factory('Command', function ($resource) {
        var Command = $resource('/api/commands/:commandId/', { commandId: '@uuid' },
            {
                query: { method: 'GET', isArray: false },
                byDevice: {method: 'GET', url: '/api/commands?device=:deviceId', isArray: false }
            }
        );
        return Command;
    });
