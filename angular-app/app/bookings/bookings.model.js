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
    this.batch_process = batch_process;
    this.account = account;
    this.dashboard = dashboard;

    function dashboard(){
      location.path('/dashboard');
    }

    function account(){
      location.path('/account');

    }

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
        setTimeout(function(){
          self.activate();
          self.chosen = {};
          LxDialogService.close('full_details');
          LxNotificationService.info('Booking request rejected');
        }, 1000);
      });

    }

    function accept_booking(booking){
      var self = this;
      var self = this;
      var now = moment(new Date()); //todays date
      var pickup_date = moment(booking.pickup_date,'M/D/YYYY'); // another date
      var duration = moment.duration(pickup_date.diff(now));
      var days = duration.asDays() + 1;
      console.log(Math.round(days));
      if(Math.round(days)<0){
        var params = {'expired': true};
        self.loading.watch(BookingRest.expired(params, booking.key.urlsafe))
        .success(function(d){
          setTimeout(function(){
            self.activate();
            self.chosen = {};
            LxNotificationService.error("You cannot accept this booking anymore!");
            LxDialogService.close('full_details');
            }, 1000);
        });

      }else{
        var data = {"approved": true, "rejected": false};
        self.loading.watch(BookingRest.update(booking.key.urlsafe, data))
        .success(function(d){
          setTimeout(function(){
            self.activate();
            self.chosen = {};
            LxDialogService.close('full_details');
            LxNotificationService.info('Booking request approved');
          }, 1000);
        });

      }

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

    function batch_process(action){
      var self = this;
      self.loading.watch(BookingRest.batch_process(self.chosen, action))
      .success(function(d){
        setTimeout(function(){
          self.activate();
          self.chosen = {};
          LxNotificationService.info('Selected booking request ' + action);
        }, 1000);
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
