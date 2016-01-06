(function(angular) {
  'use strict';

  angular
    .module('admin.services')
    .service('RequestModel', requestModel);

  requestModel.$inject = [
    '$location',
    'loading',
    'passive_messenger',
    'pubsub',
    'RequestsREST',
    'CertificatesREST',
    'LxDialogService',
  ];

  function requestModel(location, loading, passive_messenger, pubsub, RequestsREST, CertificatesREST, LxDialogService) {

    this.loading = loading.new();
    this.isBusy = isBusy;
    this.requestListing = Requests;
    this.vendors;
    this.view = view;
    this.opendDialog = opendDialog;
    this.files;
    this.show_file = show_file;

    function Requests(){
      var self = this;
      self.loading.watch(RequestsREST.list())
      .success(function(d){
        console.log(d[0]);
        self.vendors = d;
      });

    }

    function view(data){
      var self = this;
      self.opendDialog('test');
      // console.info(data);
      self.files = data;
    }

    function show_file(key){
      var self = this;
      self.loading.watch(CertificatesREST.get(key))
      .success(function(d){
        console.log(d);
        document.getElementById("show_here").src = d.image_serving_url;
      });

    }

    function opendDialog(dialogId) {
      LxDialogService.open(dialogId);
    };


    function isBusy() {
      return !!this.loading._futures.length;
    }

  }
})(window.angular);
