(function(angular) {
  'use strict';

  angular
    .module('app.controllers')
    .controller('Dashboard', userCtrl)

  userCtrl.$inject = [
    'CarModel',
    '$scope',
  ];

  function userCtrl(CarModel, $scope) {

    var user = this;
    user.loading = CarModel.loading;
    user.isBusy = isBusy;
    user.model = CarModel;


    function activate() {
      CarModel.activate();
    }

    activate();

    function isBusy() {
      return !!user.loading._futures.length;
    }

  }

})(window.angular);
