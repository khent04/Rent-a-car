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
    this.cancel_booking = cancel_booking;


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

    function rateFunction(key, rating, vendor) {
      var self = this;
      self.loading.watch(RentalREST.rate(key, rating, vendor))
      .success(function(d){
        setTimeout(function(){
        self.activate();
        }, 500);
      })
    }

    function cancel_booking(booking){
      var self = this;
      var now = moment(new Date()); //todays date
      var pickup_date = moment(booking.pickup_date,'M/D/YYYY'); // another date
      var duration = moment.duration(pickup_date.diff(now));
      var days = duration.asDays() + 3; //its just a work around to solve the problem if the current date is atleast a day before the pick up date
      console.log(Math.round(days));
      if(Math.round(days)<0){
        LxNotificationService.error("Cancelation atleast a day before!");
      }else{
        self.loading.watch(RentalREST.cancel_booking(booking))
        .success(function(d){
          self.activate();
        });
      }
    }



  }

})(window.angular);


