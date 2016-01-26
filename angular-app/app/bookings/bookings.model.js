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
    this.accept_booking = accept_booking;
    this.choose = choose;
    this.chosen = {};
    this.checker = checker;
    this.batch_accept = batch_accept;

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
      var data = {"rejected": true, "approved": false};
      self.loading.watch(BookingRest.update(key, data))
      .success(function(d){
        console.log(d);
      });

    }

    function accept_booking(key){
      var self = this;
      var data = {"approved": true, "rejected": false};
      self.loading.watch(BookingRest.update(key, data))
      .success(function(d){
        console.log(d);
      });

    }

    function choose(car){
      var self = this;
      if(car in self.chosen){
        delete self.chosen[car];
      }else{
          self.chosen[car] = true;
      }
      console.info(self.chosen);

    }

    function checker(){
      var self = this;
      if(Object.keys(self.chosen).length===0)
        return true;
      else
        return false;
    }

    function batch_accept(){
      var self = this;
      self.loading.watch(BookingRest.batch_accept(self.chosen))
      .success(function(d){
        console.log(d);
      });
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
