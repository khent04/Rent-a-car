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
      return $http.get(base);
    };

    this.get = function(params) {
      return $http.get(base, params);
    }

  }

})(window.angular);
