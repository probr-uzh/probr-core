'use strict';

angular.module('probrApp')
    .factory('Command', function (djResource) {
        var Command = djResource('/api/commands/:commandId/', {commandId: '@id'},
            {}
        );
        return Command;
    });
