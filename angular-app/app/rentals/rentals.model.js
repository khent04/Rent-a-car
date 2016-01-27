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
    this.to_home = to_home;
    this.to_account = to_account;
    this.opendDialog = opendDialog;
    this.closingDialog = closingDialog;
    this.rentals;
    this.rateFunction = rateFunction;


    function activate(){
      var self = this;
      self.loading.watch(RentalREST.list(store.get('profile').email))
      .success(function(d){
        self.rentals = d;
        console.log(d);
      });

    }

    function to_home(){
      location.path('/home');
    }

    function to_account(){
      location.path("/account");
    }

    function opendDialog(dialogID){
      LxDialogService.open(dialogID);
    }

    function closingDialog(){

    }

    function isBusy() {
      return !!this.loading._futures.length;

    }

    function rateFunction(key, rating) {
      // console.log('Rating selected: ' + rating);
      var self = this;
      self.loading.watch(RentalREST.rate(key, rating))
      .success(function(d){
        setTimeout(function(){
        self.activate();
        }, 500);
      })
    }



  }

})(window.angular);


