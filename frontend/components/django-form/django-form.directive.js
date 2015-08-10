'use strict';

/**
 * Removes server error when user updates input
 */
angular.module('boilerDjangoForm', []);
angular.module('boilerDjangoForm')
    .directive('djangoForm', function () {
        return {
            restrict: 'E',
            transclude: true,
            scope: {
                name: '=',
                label: '@',
                model: '=',
                form: '=',
                errors: '=',
            },
            templateUrl: '/static/components/django-form/django-form.html'
        };
    }).directive("dynamicName", function ($compile) {
        return {
            restrict: "A",
            terminal: true,
            priority: 1000,
            link: function (scope, element, attrs) {
                element.attr('name', scope.$eval(attrs.dynamicName));
                element.removeAttr("dynamic-name");
                $compile(element)(scope);
            }
        };
    }).directive('djangoError', function () {
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function (scope, element, attrs, ngModel) {
                element.on('keydown', function () {
                    return ngModel.$setValidity('django', true);
                });
            }
        };
    });

