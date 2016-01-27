(function (angular){
    'use strict';

    angular
        .module('app')
        .directive('switcher', switcher)
        .directive('toprated', toprated)

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

    function toprated(){
        return {
            link: link,
        };

        function link(scope, element, attrs){
            element.change(function(event){
                if(event.target.checked)
                    scope.home.model.filter_top_rated();
                else
                    scope.home.model.search();

                scope.$apply();
            });
        }
    }

})(window.angular);


