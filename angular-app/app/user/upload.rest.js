(function(angular) {
  'use strict';

  angular
    .module('app.services')
    .service('UploaderREST', uploaderRest);

  uploaderRest.$inject = [
    '$http',
  ];

  function uploaderRest($http) {

    var base = '/api/media';

    this.upload = function(params) {
      return $http.post(base + '/upload', params);
    };

    this.getUploadURL = function(){
      return $http.get('/api/media/get_upload_url', {});
    };

  }
})(window.angular);
