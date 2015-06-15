'use strict';

angular.module('probrApp')
    .controller('CapturesCtrl', function ($scope, Capture, resourceSocket) {

        var pageLength = 20;
        $scope.realTimeCaptures = [];

        Capture.query({ limit: pageLength }, function (resultObj) {
            $scope.captures = resultObj.results;
            $scope.capturesCount = resultObj.count;
            resourceSocket.updateResource($scope, $scope.realTimeCaptures, 'capture', 0, true);
        });
    });
;
