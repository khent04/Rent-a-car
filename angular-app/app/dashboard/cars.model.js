(function(angular) {
  'use strict';

  angular
    .module('app.services')
    .service('CarModel', carModel)

  carModel.$inject = [
    '$location',
    'loading',
    'LxDialogService',
    'LxNotificationService',
    'LxProgressService',
  ];

  function carModel (location, loading, LxDialogService, LxNotificationService, LxProgressService){

    this.loading = loading.new();
    this.isBusy = isBusy;
    this.activate = activate;
    this.account = account;
    this.download_template = download_template;

    function account(){
      location.path('/account');
    }

    function download_template(){
      window.location.href = '/users/xlsx';
    }

    function activate(){
      LxNotificationService.info('Loaded');
    }

    function isBusy() {
      return !!this.loading._futures.length;
    }

  }

})(window.angular);
