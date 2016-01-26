(function(angular) {
  'use strict';

  angular
    .module('app.services')
    .service('RentalREST', rentalREST);

  rentalREST.$inject = [
    '$http',
  ];

  function rentalREST($http) {

    var base = '/api/reservations';

    this.list = function() {
      return $http.get(base);
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
