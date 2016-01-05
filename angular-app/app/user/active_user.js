(function(angular) {
  'use strict';

  angular
    .module('app.services')
    .service('ActiveUser', activeUser)

  activeUser.$inject = [
    '$location',
    'loading',
    'passive_messenger',
    'pubsub',
    'LxDialogService',
    'LxNotificationService',
    'auth',
    'store'
  ];

  function activeUser(location, loading, passive_messenger, pubsub, LxDialogService, LxNotificationService, auth, store) {
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
    this.social_log = social_log;

    function activate(){
      var self = this;
      auth.hookEvents();
};




function social_log() {
    auth.signin({}, function (profile, token) {
      // Success callback
      store.set('profile', profile);
      store.set('token', token);
      console.log(profile);
      // $location.path('/');
    }, function (error) {
      // Error callback
      console.log(Object.keys(error));
      console.log(error.details);
    });


}





    function opendDialog(dialogId)
    {
    LxDialogService.open(dialogId);
    };

    function closingDialog()
    {
    LxNotificationService.info('Dialog closed!');
    };


    function isBusy() {
      return !!this.loading._futures.length;
    }

  }
})(window.angular);
