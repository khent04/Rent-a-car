(function(angular) {
  'use strict';

  angular
    .module('app.services')
    .service('CarRest', carRest);

  carRest.$inject = [
    '$http',
  ];

  function carRest($http) {

    var base = '/api/cars';

    this.list = function() {
      return $http.get(base + '/list');
    };

    this.get = function(params) {
      return $http.get(base, params);
    }

    this.create = function(vendor, params) {
      return $http.post(base + '/' + vendor , params);
    }

    this.list_by_vendor = function(vendor){
      return $http.get('/api/vendor_cars/' + vendor);
    }

    this.upload = function(params){
      return $http.post(base + '/upload', params);
    }

  }

})(window.angular);
