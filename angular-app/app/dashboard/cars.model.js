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
  ];

  function carModel (location, loading, LxDialogService, LxNotificationService, LxProgressService, CarRest, store){
    angular.extend(this, active_user);

    this.loading = loading.new();
    this.isBusy = isBusy;
    this.activate = activate;
    this.account = account;
    this.download_template = download_template;
    this.create = create;
    this.list_cars = list_cars;
    this.cars;
    this.view = view;

    function account(){
      location.path('/account');
    }

    function download_template(){
      window.location.href = '/users/xlsx';
    }

    function create(){
      var self = this;
      var data = {'car_model': 'Volkswagen Beetle', 'price': 1.0, 'seats': 5, 'transmission': 'Automatic'};
      self.loading.watch(CarRest.create(store.get('profile').email, data))
      .success(function(d){
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
      alert(key);
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
