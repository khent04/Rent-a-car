(function(angular) {
  'use strict';

  angular
    .module('admin.services')
    .service('RequestsREST', requestsRest);

  requestsRest.$inject = [
    '$http',
  ];

  function requestsRest($http) {

    var base = '/api/vendors';

    this.list = function() {
      return $http.get(base);
    };

    this.approve = function(params){
      return $http.put(base, params);
    };

  }

})(window.angular);
