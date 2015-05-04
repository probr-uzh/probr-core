'use strict';

angular.module('probrApp')
  .controller('NavbarCtrl', function ($scope, $location) {

    $scope.menu = [{
      'title': 'Devices',
      'link': '/devices'
    }];

    $scope.isActive = function(route) {
      return route === $location.path();
    };
  });
