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

    this.get = function(key) {
      return $http.get(base + '/:'+ key);
    };

    this.create = function(vendor, params) {
      return $http.post(base + '/' + vendor , params);
    };

    this.update = function(key, params) {
      return $http.put(base + '/:'+ key, params);
    };

    this.list_by_vendor = function(vendor){
      return $http.get('/api/vendor_cars/' + vendor);
    };

    this.upload = function(vendor, params){
      return $http.post(base + '/upload/' + vendor, params);
    };

  }

})(window.angular);
