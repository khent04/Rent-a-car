(function(angular) {
  'use strict';

  angular
    .module('app.services')
    .service('RentalREST', rentalREST);

  rentalREST.$inject = [
    '$http',
  ];

  function rentalREST($http) {

    var base = '/api/rentals';

    this.list = function(params) {
      return $http.get(base + '/' + params);
    };

    this.rate = function(key, rating, vendor) {
      // /api/rentals/:<key>/<rating>
      return $http.put(base + '/:' + key + '/' + rating + '/' + vendor);
    };

    this.cancel_booking = function(key) {
      return $http.delete(base + '/:' + key);
    };





  }

})(window.angular);
