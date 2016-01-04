(function(angular) {
  'use strict';

  angular
    .module('app.services')
    .service('ActiveUser', activeUser);

  activeUser.$inject = [
    '$location',
    'loading',
    'passive_messenger',
    'pubsub',
    'LxDialogService',
    'LxNotificationService'
  ];

  function activeUser(location, loading, passive_messenger, pubsub, LxDialogService, LxNotificationService) {
    angular.extend(this, active_user);
    LxNotificationService.info('Loaded');
    // LxNotificationService.success('Loaded');
    // LxNotificationService.error('Loaded');
    // LxNotificationService.warning('Loaded');

    this.loading = loading.new();
    this.isBusy = isBusy;
    this.activate = activate;
    this.mod = mod;
    this.opendDialog = opendDialog;
    this.closingDialog = closingDialog;

    function activate(){
      var self = this;
      console.log(active_user);

    }

    function mod(){
      alert();
      var self = this;
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
