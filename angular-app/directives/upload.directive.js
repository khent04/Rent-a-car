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
            if(event.target.value){
                scope.db.model.disable = false;
                scope.db.model.csv_filename = event.target.value.split( '\\' ).pop();
            }else{
                scope.db.model.disable = true;
                scope.db.model.csv_filename = "Choose a file";
            }
            scope.$apply();
            });
        }
    }

})(window.angular);
