'use strict';

angular.module('probrApp')
    .factory('Status', function ($resource) {
        var Status = $resource('/api/statuses/:statusId/', {statusId: '@uuid'},
            {
                query: {method: 'GET', isArray: false }
            }
        );
        return Status;
    });
