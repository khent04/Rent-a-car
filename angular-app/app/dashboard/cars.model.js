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
    LxProgressService.circular.show('primary', '#progress');

    this.loading = loading.new();
    this.isBusy = isBusy;
    this.activate = activate;
    this.account = account;
    this.download_template = download_template;
    this.list_cars = list_cars;
    this.cars;
    this.selected_car;
    this.view = view;
    this.upload = upload;
    this.disable = true;
    this.csv_filename = "Choose a file";
    this.opendDialog = opendDialog;
    this.update = update;
    this.choose = choose;
    this.chosen = {};
    this.checker = checker;
    this.remove = remove;
    this.upload_modal = upload_modal;
    this.diag_close = diag_close;
    this.bookings = bookings;

    function diag_close(){
      var self = this;
      self.csv_filename = "Choose a file";
      self.disable = true;
    }

    function bookings(){
      location.path('/bookings');
    }

    function account(){
      location.path('/account');

    }

    function download_template(){
      window.location.href = '/users/xlsx';

    }

    function checker(){
      var self = this;
      if(Object.keys(self.chosen).length===0)
        return true;
      else
        return false;
    }

     function choose(car){
      var self = this;
      if(car in self.chosen){
        delete self.chosen[car];
      }else{
          self.chosen[car] = true;
      }
      console.info(self.chosen);

    }

    function remove(){
      var self = this;
      self.loading.watch(CarRest.remove(self.chosen))
      .success(function(d){
        console.info(d);
        setTimeout(function(){
          self.list_cars();
          self.chosen = {};
          LxNotificationService.info('Selected Cars removed!');
        }, 500);
      });
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
      var self = this;
      self.loading.watch(CarRest.get(key))
      .success(function(d){
        self.selected_car = d;
        self.opendDialog('view');
      });

    }

    function upload_modal(){
      var self = this;
      self.opendDialog('upload');
    }

    function update(){
      var self = this;
      console.log(self.selected_car);
      var count = 0;
      if(self.selected_car.car_model===""||self.selected_car.car_model === undefined|| self.selected_car.car_model === null){
        count++;
      }
      if(self.selected_car.price===""||self.selected_car.price === undefined|| self.selected_car.price === null){
        count++;
      }
      if(count===0){
        var data = {
          car_model: self.selected_car.car_model,
          seats: self.selected_car.seats,
          price: self.selected_car.price,
          transmission: self.selected_car.transmission,
          availability: self.selected_car.availability,
          location: self.selected_car.location,
          trunk_capacity: self.selected_car.trunk_capacity,
          air_conditioned: self.selected_car.air_conditioned,
          mileage: self.selected_car.mileage,
          age: self.selected_car.age,
        };
        // angular.forEach(data, function(val, key){
        //   if(val===undefined||val==="")
        //     data[key] = null;
        // });

        self.loading.watch(CarRest.update(self.selected_car.key.urlsafe, data))
        .success(function(d){
          console.log(d);
          setTimeout(function(){
          self.list_cars();
          self.chosen = {};
          LxDialogService.close('view');
          }, 500)
        });
      }


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
        self.disable = true;
        setTimeout(function(){
          self.list_cars();
         self.csv_filename = "Choose a file";
          LxDialogService.close('upload');
          }, 1000)
      })

    }

    function chunkFn(results){
      promises.push($q);
      CarRest.upload(store.get('profile').email, results.data);
      console.log(results);

    }

    function errorFn(error){
      console.log("ERROR:", error);

    }



    function activate(){
      var self = this;
      self.list_cars();
      LxNotificationService.info('Loaded');

    }

    function opendDialog(dialogId) {
      LxDialogService.open(dialogId);

    };

    function closingDialog(){

    }


    function isBusy() {
      return !!this.loading._futures.length;

    }


  }

})(window.angular);
