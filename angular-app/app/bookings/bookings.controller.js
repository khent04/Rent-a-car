(function(angular) {
  'use strict';

  angular
    .module('app.controllers')
    .controller('Bookings', bookingsCtrl)

  bookingsCtrl.$inject = [
    'BookingModel',
    '$scope',
  ];

  function bookingsCtrl(BookingModel, $scope) {

    var user = this;
    user.loading = BookingModel.loading;
    user.isBusy = isBusy;
    user.model = BookingModel;

    function activate() {
      BookingModel.activate();
    }

    activate();

    function isBusy() {
      return !!user.loading._futures.length;
    }

  }

})(window.angular);
