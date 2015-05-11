'use strict';

angular.module('probrApp')
  .config(function ($stateProvider) {
    $stateProvider
      .state('dashboard', {
        url: '/',
        templateUrl: 'static/app/dashboard/dashboard.html',
        controller: 'DashboardCtrl'
      });
  });