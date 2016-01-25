(function(angular) {
    'use strict';

    angular
        .module('app')
        .config(routes);

    routes.$inject = ['$routeProvider', '$locationProvider'];

    function routes($routeProvider, $locationProvider) {

        $routeProvider
            .when('/login', {
                templateUrl: '/ng/templates/app-user-login.html',
                controller: 'Users',
                controllerAs: 'user',
            })
            .when('/account', {
                templateUrl: '/ng/templates/app-user-account.html',
                controller: 'Account',
                controllerAs: 'ac',
            })
            .when('/dashboard', {
                templateUrl: '/ng/templates/app-cars-dashboard.html',
                controller: 'Dashboard',
                controllerAs: 'db',
            })
            .when('/home', {
                templateUrl: '/ng/templates/app-renter-home.html',
                controller: 'Home',
                controllerAs: 'home',
            })

        $locationProvider.html5Mode(false);
    }
})(window.angular);
