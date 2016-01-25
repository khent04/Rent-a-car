(function(angular) {
  'use strict';

  angular
    .module('app.services')
    .service('BookingModel', bookingModel)

  bookingModel.$inject = [
    '$location',
    'loading',
    'LxDialogService',
    'LxNotificationService',
    'LxProgressService',
    'BookingRest',
    'store',
    '$q',
  ];

  function bookingModel (location, loading, LxDialogService, LxNotificationService, LxProgressService, BookingRest, store, $q){
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
