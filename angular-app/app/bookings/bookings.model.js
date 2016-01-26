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
    this.pending_requests;
    this.view = view;
    this.selected_;
    this.opendDialog = opendDialog;
    this.closingDialog = closingDialog;
    this.reject_booking = reject_booking;
    this.approve_booking = approve_booking;


    function activate(){
      var self = this;
      self.loading.watch(BookingRest.pending_list())
      .success(function(d){
        console.log(d);
        self.pending_requests = d;
      });
    }

    function view(key){
      var self = this;
      self.loading.watch(BookingRest.get(key))
      .success(function(d){
        console.log(d);
        self.selected_ = d;
        self.opendDialog('full_details');
      });

    }

    function reject_booking(key){
      var self = this;
      var data = {"rejected": true};
      self.loading.watch(BookingRest.update(key, store.get('profile').email, data))
      .success(function(d){
        console.log(d);
      });

    }

    function approve_booking(){

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
