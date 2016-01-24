(function(angular) {
  'use strict';

  angular
    .module('app.services')
    .service('CarModel', carModel)

  carModel.$inject = [
    '$location',
    'loading',
    'LxDialogService',
    'LxNotificationService',
    'LxProgressService',
    'CarRest',
    'store',
    '$q',
  ];

  function carModel (location, loading, LxDialogService, LxNotificationService, LxProgressService, CarRest, store, $q){
    angular.extend(this, active_user);
    // LxProgressService.circular.show('primary', '#progress');


    this.loading = loading.new();
    this.isBusy = isBusy;
    this.activate = activate;
    this.account = account;
    this.download_template = download_template;
    this.list_cars = list_cars;
    this.cars;
    this.view = view;
    this.upload = upload;
    this.disable = true;
    this.csv_filename = "Chosose a file";

    function account(){
      location.path('/account');
    }

    function download_template(){
      window.location.href = '/users/xlsx';
    }


    function list_cars(){
      var self = this;
      self.loading.watch(CarRest.list_by_vendor(store.get('profile').email))
      .success(function(d){
        console.info(d);
        self.cars = d;
      });

    }

    function view(key){
      alert(key);
    }

    var promises = [];

    function upload(){
      var self = this;
      Papa.LocalChunkSize = 10000;
      $('#file-5').parse({
        config: {
        header: true,
        chunk: chunkFn,
        error: errorFn,
        skipEmptyLines: true
        },
        before: function(file, inputElem)
        {
        console.log("Parsing file:", file);
        }
      });

      self.loading.watch($q.all(promises))
      .then(function(){
         LxNotificationService.success('Upload success!');
      })

    }

    function chunkFn(results){
      promises.push($q);
      CarRest.upload(store.get('profile').email, results.data);
      console.log(results);
    }

    function errorFn(error)
    {
      console.log("ERROR:", error);
    }



    function activate(){
      var self = this;
      self.list_cars();
      LxNotificationService.info('Loaded');
    }

    function isBusy() {
      return !!this.loading._futures.length;
    }


  }

})(window.angular);
