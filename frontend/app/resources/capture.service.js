'use strict';

angular.module('probrApp')
    .factory('Capture', function ($resource) {
        var Capture = $resource('/api/captures/:captureId/', {captureId: '@uuid'},
            {
                query: {method: 'GET', isArray: false},
            }
        );
        return Capture;
    });
