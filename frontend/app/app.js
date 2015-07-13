'use strict';

angular.module('probrApp', [
    'ngCookies',
    'ui.router',
    'ui.bootstrap',
    'ngResource',
    'angular-websocket',
    'chart.js',
    'ui.ace',
    'angularMoment',
    'luegg.directives',
]).config(function ($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider, $resourceProvider) {
    $urlRouterProvider.otherwise('devices');
    $locationProvider.html5Mode({enabled: true, requireBase: true, rewriteLinks: true});

    $resourceProvider.defaults.stripTrailingSlashes = false;
    $httpProvider.interceptors.push('authInterceptor');

})

    .factory('authInterceptor', function ($rootScope, $q, $cookies, $location) {
        return {
            // Add authorization token to headers
            request: function (config) {
                config.headers = config.headers || {};
                if ($cookies.getObject('token')) {
                    config.headers.Authorization = 'JWT ' + $cookies.getObject('token');
                }
                return config;
            },

            // Intercept 401s and redirect you to login
            responseError: function (response) {
                if (response.status === 401) {
                    $location.path('/web/login');
                    // remove any stale tokens
                    $cookieStore.remove('token');
                    return $q.reject(response);
                }
                else {
                    return $q.reject(response);
                }
            }
        };
    })

    .run(function ($rootScope, resourceSocket) {
        resourceSocket.connect();
    })
;
