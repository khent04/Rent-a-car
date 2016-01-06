(function(angular) {
  'use strict';

  angular
    .module('app.services')
    .service('RequestsREST', requestsRest);

  requestsRest.$inject = [
    '$http',
  ];

  function requestsRest($http) {

    var base = '/api/requests';

    this.list = function() {
      return $http.get(base);
    };

    this.submit = function(params) {
      return $http.post(base, params);
    }

  }

})(window.angular);
