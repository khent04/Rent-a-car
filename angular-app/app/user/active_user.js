(function(angular) {
  'use strict';

  angular
    .module('app.services')
    .service('ActiveUser', activeUser)

  activeUser.$inject = [
    'UsersREST',
    '$location',
    'loading',
    'passive_messenger',
    'pubsub',
    'LxDialogService',
    'LxNotificationService',
    'auth',
    'store',
    'jwtHelper',
    'FileUploader',
    'UploaderREST',
    'LxProgressService',

  ];

  function activeUser(UsersREST, location, loading, passive_messenger, pubsub, LxDialogService, LxNotificationService, auth, store, jwtHelper, FileUploader, UploaderREST, LxProgressService) {
    angular.extend(this, active_user);
    // LxNotificationService.info('Loaded');
    // LxNotificationService.success('Loaded');
    // LxNotificationService.error('Loaded');
    // LxNotificationService.warning('Loaded');

    this.loading = loading.new();
    this.isBusy = isBusy;
    this.activate = activate;
    this.opendDialog = opendDialog;
    this.closingDialog = closingDialog;
    this.social_login = social_login;
    this.social_logout = social_logout;
    this.oauth = oauth;
    this.vendor_login = vendor_login;
    this.account = account;
    this.update = update;
    this.auth = auth;
    this.account_data;
    this.country = ["China", "India", "Japan", "Malaysia", "Myanmar", "Philippines", "Singapore", "South", "Thailand", "Vietnam"];
    this.fleet = ['0-50','50-100', '100-200', '200-500', '500+'];
    this.dashboard = dashboard;
    this.to_account = to_account;
    this.to_home = to_home;
    this.to_my_rentals = to_my_rentals;

    function dashboard(){
      location.path('/dashboard');
    }

    function to_home(){
      location.path('/home');

    }

    function to_account(){
      location.path("/account");
    }

    function to_my_rentals(){
      location.path("/my_rentals");
    }

    this.vendor_request = vendor_request;
    var certificates = [];

    this.uploader = new FileUploader();

    this.uploader.filters.push({
            name: 'customFilter',
            fn: function(item /*{File|FileLikeObject}*/, options) {
                return this.queue.length < 10;
            }
        });

        this.uploader.onWhenAddingFileFailed = function(item /*{File|FileLikeObject}*/, filter, options) {
            console.warn('onWhenAddingFileFailed', item, filter, options);
        };
        this.uploader.onAfterAddingFile = function(fileItem) {
            console.info('onAfterAddingFile', fileItem);
            var importfile = fileItem;
            UploaderREST.getUploadURL()
            .success(function(data, status, headers, config){
                importfile.url = data.upload_url;
                // importfile.upload();
                console.log('success', importfile);

            }).error(function(data, status, headers, config){
                console.log('fail');
            });

        };
        this.uploader.onAfterAddingAll = function(addedFileItems) {
            console.info('onAfterAddingAll', addedFileItems);
        };
        this.uploader.onBeforeUploadItem = function(item) {
            console.info('onBeforeUploadItem', item);
        };
        this.uploader.onProgressItem = function(fileItem, progress) {
            console.info('onProgressItem', fileItem, progress);
        };
        this.uploader.onProgressAll = function(progress) {
            console.info('onProgressAll', progress);
        };
        this.uploader.onSuccessItem = function(fileItem, response, status, headers) {
            console.info('onSuccessItem', fileItem, response, status, headers);
        };
        this.uploader.onErrorItem = function(fileItem, response, status, headers) {
            console.info('onErrorItem', fileItem, response, status, headers);
        };
        this.uploader.onCancelItem = function(fileItem, response, status, headers) {
            console.info('onCancelItem', fileItem, response, status, headers);
        };
        this.uploader.onCompleteItem = function(fileItem, response, status, headers) {
            console.info('onCompleteItem', response); // --------- urlsafe to be save!!!!!!!!!!!
            certificates.push(response)
        };
        this.uploader.onCompleteAll = function() {
            console.info('onCompleteAll');
            // LxProgressService.linear.hide();
            LxProgressService.circular.hide();
            LxNotificationService.success('File Uploaded');
        };

        this.showCircularProgress = function(){
          LxProgressService.circular.show('primary', '#progress');
        };

    function activate(){
      var self = this;
      if(active_user===null){
        self.oauth('Renter');
      }

    }

    function oauth(Role){
      auth.hookEvents();
      var self = this;
      var token = store.get('token');
      if (token) {
        if (!jwtHelper.isTokenExpired(token)) {
          if (!auth.isAuthenticated) {
            auth.authenticate(store.get('profile'), token);
          }
        }
      } else {
        self.social_login(Role);
      }

    }

    function social_login(Role) {
      var self = this;

      auth.signin({}, function (profile, token) {
        store.set('profile', profile);
        store.set('token', token);
        console.log(self.auth.profile);
        var data = {'email': self.auth.profile.email,
                    'first_name': self.auth.profile.given_name,
                    'last_name': self.auth.profile.family_name,
        };

        self.loading.watch(UsersREST.create(data, Role))
        .success(function(d){
          console.info(d);
          location.path("/account");
        });

      }, function (error) {
        console.warn(Object.keys(error));
        console.warn(error.details);
      });

    }

    function social_logout() {
      auth.signout();
      store.remove('profile');
      store.remove('token');
      location.path('/login');

    }

    function vendor_login(){
      var self = this;
      self.oauth('Vendor');
    }

    function account(){
      var self = this;
      auth.hookEvents();
      var token = store.get('token');
      if (token) {
        if(jwtHelper.isTokenExpired(token)){
          location.path('/login');
        }else{
          // console.log(store.get('profile'));
          // self.account_data = store.get('profile');
          // ----- get data from data store
          self.loading.watch(UsersREST.get(store.get('profile').email))
          .success(function(d){
            console.info(d);
            self.account_data = d;
          })
        }
      }else{
        location.path('/login');
      }
    }

    function vendor_request(){
      var self = this;
      // alert();
      console.log(self.account_data);
      var data = {
        'first_name': self.account_data.first_name,
        'last_name': self.account_data.last_name,
        'contact_number': self.account_data.contact_number,
        'company': self.account_data.company,
        'unit_number': self.account_data.unit_number,
        'street_address': self.account_data.street_address,
        'country': self.account_data.country,
        'fleet_size': self.account_data.fleet_size,
        'abouts': self.account_data.abouts,
        'company_rules': self.account_data.company_rules,
        'credentials': certificates,
        'postal_code': self.account_data.postal_code
      };

      console.log(Object.keys(data));
      var incomplete = false;

      if(Object.keys(data).length==12){
        angular.forEach(data, function(val, key){
          if(val==="" || val === null)
            incomplete = true;
         });

        if(incomplete)
          // alert('kulang!');
        self.opendDialog('test');
        else{
          data['submitted'] = true;
          self.loading.watch(UsersREST.update(self.account_data.email, data))
          .success(function(d){
          console.log(d);
          LxNotificationService.success('Information Saved');
          });
        }
      }

    }

    function update(){
      var self = this;
      console.log(self.account_data);
      var data = {
        first_name: self.account_data.first_name,
        last_name: self.account_data.last_name,
        contact_number: self.account_data.contact_number,
        postal_code: self.account_data.postal_code,
        user_type: self.account_data.user_type
      };
                self.loading.watch(UsersREST.update(self.account_data.email, data))
          .success(function(d){
          console.log(d);
          LxNotificationService.success('Information Saved');
          });
    }

    function opendDialog(dialogId) {
      LxDialogService.open(dialogId);

    };

    function closingDialog() {
      // LxNotificationService.info('Dialog closed!');

    };

    function isBusy() {
      return !!this.loading._futures.length;
    }

  }
})(window.angular);
