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
    this.dropdowns = [];
    this.toModel = toModel;

    function Requests(){
      var self = this;
      self.loading.watch(RequestsREST.list())
      .success(function(d){
        console.log(d[0]);
        self.vendors = d;
      });

    }

    function view(data){  //opening of dialog
      var self = this;
      self.dropdowns = [];
      self.opendDialog('test');
      self.files = data;
      angular.forEach(data, function(val, key){
        key++;
        self.dropdowns.push({urlsafe: val.__key__, tmp_name: 'file_' + key});
      });

    }

    function show_file(data){
      var self = this;
      self.loading.watch(CertificatesREST.get(data.urlsafe))
      .success(function(d){
        document.getElementById("show_here").src = d.image_serving_url;
      });

    }

    function toModel(data, callback){
      var self = this;
      self.show_file(data);
      if (data){
      callback(data.Title);
      }else{
      callback();
      }
    }

    function opendDialog(dialogId) {
      LxDialogService.open(dialogId);
    };


    function isBusy() {
      return !!this.loading._futures.length;
    }

  }
})(window.angular);
