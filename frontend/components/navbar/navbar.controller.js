'use strict';

angular.module('probrApp')
    .controller('NavbarCtrl', function ($scope, $location, Auth) {

        $scope.menu = [
            {
                'title': 'Devices',
                'link': '/web/devices'
            },
            {
                'title': 'Captures',
                'link': '/web/captures'
            }
        ];

        $scope.isActive = function (route) {
            return route === $location.path();
        };

        $scope.isLoggedIn = Auth.isLoggedIn;
        $scope.getCurrentUser = Auth.getCurrentUser;

        $scope.logout = function () {
            Auth.logout();
            $location.path('/login');
        };

        $scope.isActiveRoot = function (route) {
            var subStr = $location.path().split("/")[1];
            return route.indexOf(subStr.substr(0, subStr.length - 1)) !== -1;
        };

    });
