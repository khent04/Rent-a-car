(function(angular) {
  'use strict';

  angular
    .module('admin.services')
    .service('CertificatesREST', certificatesREST);

  certificatesREST.$inject = [
    '$http',
  ];

  function certificatesREST($http) {

    var base = '/api/certificates';

    this.list = function() {
      return $http.get(base);
    };

    this.get = function(key) {
      return $http.get(base +'/'+ key);
    }

  }

})(window.angular);
