(function(angular) {
  'use strict';

  angular
    .module('app.services')
    .service('HomeModel', homeModel)

  homeModel.$inject = [
    '$location',
    'loading',
    'LxDialogService',
    'LxNotificationService',
    'LxProgressService',
    'HomeREST',
    'store',
    '$q',
  ];

  function homeModel (location, loading, LxDialogService, LxNotificationService, LxProgressService, CarRest, store, $q){
    angular.extend(this, active_user);
    LxProgressService.circular.show('primary', '#progress');

    this.loading = loading.new();
    this.isBusy = isBusy;
    this.activate = activate;



    function activate(){

    }

    function isBusy() {
      return !!this.loading._futures.length;

    }


  }

})(window.angular);
