(function () {
    angular.module('flaederGamesApp')
        .directive('fldrPlayerRegister', [function () {
            return {
                restrict: 'E',
                templateUrl: '/app/components/home/home.register.template.html',
            };
    }]);
})();
