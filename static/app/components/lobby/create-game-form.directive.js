(function () {
    angular.module('flaederGamesApp')
        .directive('fldrCreateGameForm', [function () {
            return {
                restrict: 'E',
                templateUrl: '/app/components/lobby/create-game-form.template.html'
            };
    }]);
})();
