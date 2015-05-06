'use strict';

angular.module('probrApp')
  .controller('NavbarCtrl', function ($scope, $location) {

    $scope.menu = [{
      'title': 'Manage Devices',
      'link': '/devices'
    },
    {
      'title': 'Schedule Commands',
      'link': '/commands'
    }];

    $scope.isActive = function(route) {
      return route === $location.path();
    };
  });
