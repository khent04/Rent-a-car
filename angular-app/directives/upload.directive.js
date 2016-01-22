(function (angular){
    'use strict';

    angular
        .module('app')
        .directive('quired', quired)

    function quired(){
        return {
            link: link,
        };

        function link(scope, element, attrs){
           element.change(function(){
                scope.db.model.disable = false;
                scope.$apply();
            })
        }
    }

})(window.angular);
