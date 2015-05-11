'use strict';

angular.module('probrApp', [
    'ui.router',
    'ui.bootstrap',
    'djangoRESTResources',
    'angular-websocket',
    'chart.js'
])
    .config(function ($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider) {
        $urlRouterProvider.otherwise('/');
        $locationProvider.html5Mode(true);
    })

    .run(function ($rootScope) {

    })
;
