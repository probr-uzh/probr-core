'use strict';

angular.module('probrApp')
    .controller('CapturesCtrl', function ($scope, Capture, resourceSocket) {
        Capture.query({}, function (resultObj) {
            $scope.captures = resultObj.results;
            $scope.numberOfCaptures = resultObj.count;
            resourceSocket.updateResource($scope, $scope.captures, 'capture', 'uuid');
        });
    });
;
