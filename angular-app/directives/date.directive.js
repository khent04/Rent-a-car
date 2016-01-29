(function(angular) {
  'use strict';

  angular
    .module('app')
    .directive("datemin", datemin);

  datemin.$inject = ['$compile'];

  function datemin($compile){
    return {
      scope: true,
      restrict: 'A',
      link: function (scope, elm, attrs) {
          var limit = attrs.limit;
          if (limit == 'today'){
            $elm.attr('max', moment().format("YYYY-MM-DD"));
          }
      }
    };
  }

})(window.angular);
