'use strict';

angular.module('probrApp')
    .factory('Capture', function ($resource) {
        var Capture = $resource('/api/captures/:captureId/', {captureId: '@uuid'},
            {
            }
        );
        return Capture;
    });
