'use strict';

angular.module('probrApp')
    .factory('CommandTemplate', function ($resource) {
        var CommandTemplate = $resource('/api/commandtemplates/:commandTemplateId/', { commandTemplateId: '@uuid' },
            {
                query: { method: 'GET', isArray: false },
                update: { method: 'PUT', isArray: false },
                delete: { method: 'DELETE', isArray: false }
            }
        );
        return CommandTemplate;
    });
