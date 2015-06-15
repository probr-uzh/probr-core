'use strict';

angular.module('probrApp')
    .controller('CapturesCtrl', function ($scope, Capture, resourceSocket) {
        Capture.query({limit: 50}, function (resultObj) {
            $scope.captures = resultObj.results;
            resourceSocket.updateResource($scope, $scope.captures, 'capture', 'uuid', 50);
        });
    });
;
