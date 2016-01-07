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
    'LxNotificationService',
  ];

  function requestModel(location, loading, passive_messenger, pubsub, RequestsREST, CertificatesREST, LxDialogService, LxNotificationService) {

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
    this.choose = choose;
    this.chosen = {};
    this.checker = checker;
    this.approve = approve;


    function checker(){
      var self = this;
      if(Object.keys(self.chosen).length===0)
        return true;
      else
        return false;
    }

    function Requests(){
      var self = this;
      self.loading.watch(RequestsREST.list())
      .success(function(d){
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

    function choose(user){
      var self = this;
      if(user in self.chosen){
        delete self.chosen[user];
      }else{
          self.chosen[user] = true;
      }
      console.info(self.chosen);

    }

    function approve(){
      var self = this;
      self.loading.watch(RequestsREST.approve(Object.keys(self.chosen)))
      .success(function(response){
        setTimeout(function(){
          LxNotificationService.success('Vendor request approved!');
          location.path("/xbjsd");
        }, 500);
      })

    }

    function opendDialog(dialogId) {
      LxDialogService.open(dialogId);
    };


    function isBusy() {
      return !!this.loading._futures.length;
    }

  }
})(window.angular);
