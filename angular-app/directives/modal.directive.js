(function (angular){
    'use strict';

    angular
        .module('app')
        .directive('ckbox', ckbox)
        .directive('checker', checker)

    function ckbox(){
        return {
            link: link,
        };

        function link(scope, element, attrs){
            element.change(function(event){
                if(event.target.checked)
                    scope.db.model.selected_car.mileage = "Unlimited";
                else
                    delete scope.db.model.selected_car.mileage;

            });
        }
    }

    function checker(){
        return {
            link: link,
        }

        function link(scope, element, attrs){
            element.click(function(event){
                if(scope.db.model.selected_car.car_model===""){
                    $('#car_model').css("visibility", "visible");
                    $('.car_model').focus();
                }
                else{
                    $('#car_model').css("visibility", "hidden");
                }

                if(scope.db.model.selected_car.price===""){
                    $('#price').css("visibility", "visible");
                    $('.price').focus();
                }else{
                    $('#price').css("visibility", "hidden");
                }
            });
        }
    }

})(window.angular);


