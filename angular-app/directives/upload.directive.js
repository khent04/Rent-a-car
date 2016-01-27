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
                if(event.target.value.split( '\\' ).pop().split('.')[1]==="csv"){
                    scope.db.model.disable = false;
                    scope.db.model.csv_filename = event.target.value.split( '\\' ).pop();
                }else{
                    scope.db.model.errs("Uploaded file format is invalid. Please remove the file, open in Excel, and save as a CSV (Comma-delimited) (*.csv) file type.");
                }
            }else{
                scope.db.model.disable = true;
                scope.db.model.csv_filename = "Choose a file";
            }
            scope.$apply();
            });
        }
    }

})(window.angular);
