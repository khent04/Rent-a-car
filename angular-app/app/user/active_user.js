(function(angular) {
  'use strict';

  angular
    .module('app.services')
    .service('ActiveUseraa', activeUser);

  activeUser.$inject = [
    '$location',
    'loading',
    'passive_messenger',
    'pubsub',
  ];

  function activeUser(location, loading, passive_messenger, pubsub) {

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
