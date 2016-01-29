(function(angular) {
  'use strict';

  angular
    .module('cs.utilities', [
      'cs.pubsub',
      'cs.passive-messenger',
      'cs.loading',
      'cs.modal',
    ]);

  angular
    .module('admin.services', [
      'cs.utilities',
    ]);

  angular
    .module('admin.controllers', [
      'admin.services',
    ]);

  angular
    .module('admin.directives', [
      'cs.utilities',
    ]);

  angular
    .module('admin', [
      'admin.services',
      'admin.directives',
      'admin.controllers',
      'ngSanitize',
      'ngRoute',
      'ui.select',
      'lumx',
    ])
    .run(admin);

  admin.$inject = ['$log', 'passive_messenger', '$timeout', '$rootScope'];

  function admin($log, passive_messenger, $timeout, $rootScope) {
    $log.info('Angular Admin Loaded');
    $timeout(function() { passive_messenger.success('Loaded'); });
    $rootScope.ngLoadingFinished = true;
  }
})(window.angular);
