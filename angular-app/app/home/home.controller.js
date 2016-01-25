(function(angular) {
  'use strict';

  angular
    .module('app.controllers')
    .controller('Home', homeCtrl)

  homeCtrl.$inject = [
    'HomeModel',
    '$scope',
  ];

  function homeCtrl(HomeModel, $scope) {

    var user = this;
    user.loading = HomeModel.loading;
    user.isBusy = isBusy;
    user.model = HomeModel;

    function activate() {
      HomeModel.activate();
    }

    activate();

    function isBusy() {
      return !!user.loading._futures.length;
    }

  }

})(window.angular);
