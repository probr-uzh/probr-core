'use strict';

angular.module('probrApp')
  .controller('LoginCtrl', function ($scope, Auth, $location) {
    $scope.user = {};
    $scope.errors = {};

    $scope.login = function(form) {
      $scope.submitted = true;

      if(form.$valid) {
        Auth.login({
          username: $scope.user.username,
          password: $scope.user.password
        })
        .then( function() {
          // Logged in, redirect to home
          $location.path('/web');
        })
        .catch( function(err) {
          $scope.errors.other = err.message;
        });
      }
    };

  });
