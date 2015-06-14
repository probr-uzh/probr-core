'use strict';

angular.module('probrApp')
    .controller('PacketsCtrl', function ($scope, resourceSocket) {
        $scope.packets = [];
        resourceSocket.updateResource($scope, $scope.packets, 'packet');
    });
;
