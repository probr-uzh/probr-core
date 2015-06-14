'use strict';

angular.module('probrApp')
    .config(function ($stateProvider) {
        $stateProvider
            .state('packets', {
                url: '/packets',
                templateUrl: '/static/app/packets/packets.html',
                controller: 'PacketsCtrl'
            });
        ;
    });