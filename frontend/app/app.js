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

        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    })

    .run(function ($rootScope) {

    })
;
