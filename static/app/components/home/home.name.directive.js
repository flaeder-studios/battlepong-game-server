(function () {
    angular.module('flaederGamesApp')
        .directive('fldrPlayerName', [function () {
            return {
                restrict: 'E',
                templateUrl: '/app/components/home/home.name.template.html',
            };
    }]);
})();
