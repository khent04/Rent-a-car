(function(angular) {
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


    this.wow = function(){
      var self = this;
      console.log(self);
    }

    function Requests(){
      var self = this;

    }


    function isBusy() {
      return !!this.loading._futures.length;
    }

  }
})(window.angular);
