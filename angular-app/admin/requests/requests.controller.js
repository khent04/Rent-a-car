(function(angular) {
  'use strict';

  angular
    .module('admin.controllers')
    .controller('Requests', requestCtrl);

  requestCtrl.$inject = [
    'RequestModel',
    'pubsub',
    '$scope',
  ];

  function requestCtrl(Request, pubsub, $scope) {

    var request = this;
    request.loading = Request.loading;
    request.list = Request.list;
    request.isBusy = isBusy;

    request.model = Request;

    function activate() {
      Request.requestListing();
    }

    activate();

    function isBusy() {
      return !!request.loading._futures.length;
    }

  }
})(window.angular);


