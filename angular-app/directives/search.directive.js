(function (angular){
    'use strict';

    angular
        .module('app')
        .directive('switcher', switcher)

    function switcher(){
        return {
            link: link,
        };

        function link(scope, element, attrs){
            element.change(function(event){
                if(event.target.checked)
                    scope.home.model.diff_location = true;
                else
                    scope.home.model.diff_location = false;

                scope.$apply();

            });
        }
    }


})(window.angular);


