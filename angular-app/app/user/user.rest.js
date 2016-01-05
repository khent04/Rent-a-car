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

    this.create = function(params, Role) {
      return $http.post(base +'/'+ Role, params);
    };

    this.get = function(email) {
      return $http.get(base + '/' +email);
    };

    this.update = function(email, params) {
      return $http.put(base + '/' + email, params);
    };

    this.ken = function(){
      return $http.get(base + '/ken');
    };

  }

})(window.angular);
