(function(angular) {
  'use strict';

  angular
    .module('app.controllers')
    .controller('Rentals', rentalsCtrl)

  rentalsCtrl.$inject = [
    'RentalModel',
    '$scope',
  ];

  function rentalsCtrl(RentalModel, $scope) {

    var user = this;
    user.loading = RentalModel.loading;
    user.isBusy = isBusy;
    user.model = RentalModel;

    function activate() {
      RentalModel.activate();
    }

    activate();

    function isBusy() {
      return !!user.loading._futures.length;
    }

  }

})(window.angular);
