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



  }

})(window.angular);
