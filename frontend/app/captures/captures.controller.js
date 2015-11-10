'use strict';

angular.module('probrApp')
    .controller('CapturesCtrl', function ($scope, Capture, resourceSocket) {

        var pageLength = 20;
        $scope.realTimeCaptures = [];

        Capture.query({}, function (resultObj) {
            $scope.captures = resultObj.results;
            $scope.capturesCount = resultObj.count;
            resourceSocket.updateResource($scope, $scope.realTimeCaptures, 'capture', 0, true);
        });
    })
    .controller('CapturesAddCtrl', function ($scope, $cookies, FileUploader) {
        $scope.formData = [];

        $scope.uploader = new FileUploader({
            url: "/api-device/captures/",
            alias: "pcap",
            headers: {"Authorization": 'JWT ' + $cookies.get('token')},
            removeAfterUpload: true
        });

        $scope.uploader.onBeforeUploadItem = function (item) {
            item.formData.push({tags: $scope.tags});
            item.formData.push({longitude: $scope.longitude});
            item.formData.push({latitude: $scope.latitude});
        };

        $scope.uploadCaptures = function (form) {
            $scope.errors = {};

            if (isNaN($scope.longitude)) {
                form['longitude'].$setValidity('django', false);
                $scope.errors.longitude = "not a number";
            }

            if (isNaN($scope.latitude)) {
                form['latitude'].$setValidity('django', false);
                $scope.errors.latitude = "not a number";
            }

            if(_.isEmpty($scope.errors)){
                console.log("uploading");

                $scope.uploader.uploadAll();
            }

        };
    });
;
