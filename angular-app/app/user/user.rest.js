(function(angular) {
  'use strict';

  angular
    .module('app.services')
    .service('UsersREST', usersRest);

  usersRest.$inject = [
    '$http',
  ];

  function usersRest($http) {

    var base = '/api/users';

    this.list = function() {
      return $http.get(base);
    };

    this.create = function(params) {
      return $http.post(base, params);
    };

    this.ken = function(){
      return $http.get(base + '/ken');
    };

  }

})(window.angular);
