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
           element.change(function(event){
                scope.db.model.disable = false;
                scope.db.model.csv_filename = event.target.value.split( '\\' ).pop();;
                scope.$apply();
            })
        }
    }

})(window.angular);
