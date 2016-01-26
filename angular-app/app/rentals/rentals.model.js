(function(angular) {
  'use strict';

  angular
    .module('app.services')
    .service('RentalModel', rentalModel)

  rentalModel.$inject = [
    '$location',
    'loading',
    'LxDialogService',
    'LxNotificationService',
    'LxProgressService',
    'RentalREST',
    'store',
    '$q',
  ];

  function rentalModel (location, loading, LxDialogService, LxNotificationService, LxProgressService, RentalREST, store, $q){
    angular.extend(this, active_user);
    LxProgressService.circular.show('primary', '#progress');

    this.loading = loading.new();
    this.isBusy = isBusy;
    this.activate = activate;
    this.opendDialog = opendDialog;
    this.closingDialog = closingDialog;

    function activate(){
      var self = this;

    }

    function opendDialog(dialogID){
      LxDialogService.open(dialogID);
    }

    function closingDialog(){

    }

    function isBusy() {
      return !!this.loading._futures.length;

    }


  }

})(window.angular);
