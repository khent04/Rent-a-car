(function(angular) {
    'use strict';

    angular
        .module('admin2')
        .config(routes);

    routes.$inject = ['$routeProvider', '$locationProvider'];

    function routes($routeProvider, $locationProvider) {

        // Your routes here!
        // $routeProvider
        //     .when('/application-settings', {
        //         templateUrl: '/ng/admin/application-settings/settings.partial.html',
        //         controller: 'Settings',
        //         controllerAs: 'set',
        //     })
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
        //     .otherwise({
        //         redirectTo: '/application-settings'
        //     });

        $locationProvider.html5Mode(false);
    }
})(window.angular);
