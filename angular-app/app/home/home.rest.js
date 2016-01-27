(function(angular) {
  'use strict';

  angular
    .module('app.services')
    .service('HomeREST', homeREST);

  homeREST.$inject = [
    '$http',
  ];

  function homeREST($http) {

    var base = '/api/home';

    this.list = function() {
      return $http.get(base);
    };

    this.search = function(params){
      return $http.post('/api/search/cars', params);
    };

    this.show_top_rated = function(params){
      return $http.post('/api/search/cars/top', params);
    };

    this.reserve = function(key, params){
      return $http.post('/api/reservations/:' + key, params);
    }


  }

})(window.angular);
