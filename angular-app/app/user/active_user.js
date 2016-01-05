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

  ];

  function activeUser(UsersREST, location, loading, passive_messenger, pubsub, LxDialogService, LxNotificationService, auth, store, jwtHelper) {
    angular.extend(this, active_user);
    LxNotificationService.info('Loaded');
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

    function activate(){
      var self = this;
      if(active_user===null){
        self.oauth();
      }

    }

    function oauth(){
      auth.hookEvents();
      var self = this;
      self.auth = auth;
      var token = store.get('token');
      if (token) {
        if (!jwtHelper.isTokenExpired(token)) {
          if (!auth.isAuthenticated) {
            auth.authenticate(store.get('profile'), token);
          }
        }
      } else {
        self.social_login();
      }

    }


    function social_login() {
      var self = this;
      auth.signin({}, function (profile, token) {
        store.set('profile', profile);
        store.set('token', token);
        var data = {'email': self.auth.profile.email,
                    'first_name': self.auth.profile.given_name,
                    'last_name': self.auth.profile.family_name,
        };

        self.loading.watch(UsersREST.create(data))
        .success(function(d){
          console.info(d);
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

    }

    function opendDialog(dialogId) {
      LxDialogService.open(dialogId);

    };

    function closingDialog() {
      LxNotificationService.info('Dialog closed!');

    };


    function isBusy() {
      return !!this.loading._futures.length;
    }

  }
})(window.angular);
