(function(angular) {
    'use strict';

    angular
        .module('app')
        .config(routes);

    routes.$inject = ['$routeProvider', '$locationProvider'];

    function routes($routeProvider, $locationProvider) {

        // Your routes here!
        $routeProvider
            .when('/login', {
                templateUrl: '/ng/templates/app-user-login.html',
                controller: 'Users',
                controllerAs: 'user',
            })
        //     .when('/users', {
        //         templateUrl: '/ng/admin/users/user.partial.html',
        //         controller: 'Users',
        //         controllerAs: 'usr',
        //     })
        //     .when('/agents', {
        //         templateUrl: '/ng/admin/agents/agent.partial.html',
        //         controller: 'Agents',
        //         controllerAs: 'agn',
        //     })
        //     .when('/vendors', {
        //         templateUrl: '/ng/admin/vendors/vendor.partial.html',
        //         controller: 'Vendors',
        //         controllerAs: 'vnd',
        //     })
        //     .when('/factories', {
        //         templateUrl: '/ng/admin/factories/factory.partial.html',
        //         controller: 'Factories',
        //         controllerAs: 'fct',
        //     })
            .otherwise({
                redirectTo: '/login'
            });

        $locationProvider.html5Mode(false);
    }
})(window.angular);
