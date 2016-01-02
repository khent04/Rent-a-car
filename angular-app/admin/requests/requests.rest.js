(function(angular) {
  'use strict';

  angular
    .module('admin.services')
    .service('RequestsREST', requestsRest);

  requestsRest.$inject = [
    '$http',
  ];

  function requestsRest($http) {

    var base = '/api/requests';

    this.list = function() {
      return $http.get(base);
    };

  }

})(window.angular);
