(function(angular, active_user) {
  'use strict';

  angular
    .module('admin')
    .config(config);

  config.$inject = [
    '$provide',
    'uiSelectConfig',
  ];

  function config($provide, uiSelectConfig) {

    active_user.is = function(comparator, role) {
      if (comparator == '=')
        return get_permission_level(role) == get_permission_level(this.role);
      if (comparator == '>')
        return get_permission_level(role) < get_permission_level(this.role);
      if (comparator == '<')
        return get_permission_level(role) > get_permission_level(this.role);
      if (comparator == '>=')
        return get_permission_level(role) <= get_permission_level(this.role);
      if (comparator == '<=')
        return get_permission_level(role) >= get_permission_level(this.role);
      if (comparator == '!=')
        return get_permission_level(role) != get_permission_level(this.role);
    };

    function get_permission_level(role) {
      if (role == "Selling Partner")
        return 10;
      if (role == "Selling Coach")
        return 20;
      else if (role == "Section Manager")
        return 30;
      else if (role == "Branch Manager")
        return 40;
      else if (role == "Operations Manager")
        return 50;
      else if (role == "Customer Experience Team")
        return 60;
      else if (role == "Admin")
        return 100;
      else
        return 0;
    }

    $provide.constant('ActiveUser', active_user);
    uiSelectConfig.resetSearchInput = true;
  }
})(window.angular, window.active_user);
