(function(angular) {
  'use strict';

  angular
    .module('app.controllers')
    .controller('Users', userCtrl)
    .controller('Account', accountCtrl);

  userCtrl.$inject = [
    'ActiveUser',
    'pubsub',
    '$scope',
  ];
  function userCtrl(ActiveUser, pubsub, $scope) {

    var user = this;
    user.loading = ActiveUser.loading;
    // user.list = user.list;
    user.isBusy = isBusy;

    user.model = ActiveUser;

    function activate() {
      ActiveUser.activate();
    }

    activate();

    function isBusy() {
      return !!user.loading._futures.length;
    }

  }

  accountCtrl.$inject = [
    'ActiveUser',
    'pubsub',
    '$scope',
  ];

    function accountCtrl(ActiveUser, pubsub, $scope) {

    var user = this;
    user.loading = ActiveUser.loading;
    // user.list = user.list;
    user.isBusy = isBusy;

    user.model = ActiveUser;

    function activate() {
      ActiveUser.account();
    }

    activate();

    function isBusy() {
      return !!user.loading._futures.length;
    }

  }





})(window.angular);
