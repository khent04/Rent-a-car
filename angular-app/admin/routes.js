(function(angular) {
    'use strict';

    angular
        .module('admin')
        .config(routes);

    routes.$inject = ['$routeProvider', '$locationProvider'];

    function routes($routeProvider, $locationProvider) {

        $routeProvider
            .when('/requests', {
                templateUrl: '/ng/templates/admin-requests.html',
                controller: 'Requests',
                controllerAs: 'rq',
            })
            .otherwise({
                redirectTo: '/requests'
            });

        $locationProvider.html5Mode(false);
    }
})(window.angular);
