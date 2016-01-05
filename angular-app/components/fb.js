(function (angular) {
    angular.module('fb', ['auth0', 'angular-storage', 'angular-jwt'])
    .config(config);

    config.$inject = ['authProvider'];

    function config(authProvider){

        authProvider.init({
        domain: 'care-rental-appspot-com.auth0.com',
        clientID: 'DxYX1KQd664RUlwZkzcXekBsGkpRXebg'
        });

    }

}(angular));
