(function(angular, active_user) {
  'use strict';

  angular
    .module('admin.services')
    .service('RequestModel', requestModel);

  requestModel.$inject = [
    '$location',
    'loading',
    'passive_messenger',
    'pubsub',
  ];

  function requestModel(location, loading, passive_messenger, pubsub) {

    this.loading = loading.new();
    this.isBusy = isBusy;
    this.requestListing = Requests;

    function isBusy() {
      return !!this.loading._futures.length;
    }

    function Requests(){
      passive_messenger.success("Controller is now working!");
    };

  }

})(window.angular, window.active_user);
