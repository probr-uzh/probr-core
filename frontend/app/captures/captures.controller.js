'use strict';

angular.module('probrApp')
    .controller('CapturesCtrl', function ($scope, Capture, resourceSocket) {
        Capture.query({}, function (resultObj) {
            $scope.captures = resultObj;
            resourceSocket.updateResource($scope, $scope.captures, 'capture');
        });
    });
;
