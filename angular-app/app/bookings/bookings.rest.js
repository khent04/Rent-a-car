(function(angular) {
  'use strict';

  angular
    .module('app.services')
    .service('BookingRest', bookingRest);

  bookingRest.$inject = [
    '$http',
  ];

  function bookingRest($http) {

    var base = '/api/home';

    this.list = function() {
      return $http.get(base);
    };

    this.search = function(params){
      return $http.post('/api/search/cars', params);
    };

    this.reserve = function(key, params){
      return $http.post('/api/reservations/' + key, params);
    }



  }

})(window.angular);
