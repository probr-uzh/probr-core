'use strict';

angular.module('probrApp')
    .config(function ($stateProvider) {
        $stateProvider
            .state('login', {
                url: '/login',
                templateUrl: '/static/app/account/login/login.html',
                controller: 'LoginCtrl'
            });
        ;
    });