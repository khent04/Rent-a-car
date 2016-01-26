(function(angular) {
  'use strict';

  angular
    .module('app.services')
    .service('BookingRest', bookingRest);

  bookingRest.$inject = [
    '$http',
  ];

  function bookingRest($http) {

    var base = '/api/reservations';

    this.list = function() {
      return $http.get(base);
    };

    this.search = function(params){
      return $http.post('/api/search/cars', params);
    };

    this.reserve = function(key, params){
      return $http.post(base + key, params);
    };

    this.pending_list = function(){
      return $http.get(base + '/pending');
    }

    this.get = function(key) {
      return $http.get(base + '/:'+ key);
    };

    this.update = function(key, params) {
      return $http.put(base + '/:'+ key, params);
    };



  }

})(window.angular);
