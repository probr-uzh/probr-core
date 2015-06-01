'use strict';

angular.module('probrApp')
    .factory('Status', function (djResource) {
        var Status = djResource('/api/statuses/:statusId/', {statusId: '@id'}

        );
        return Status;
    });
