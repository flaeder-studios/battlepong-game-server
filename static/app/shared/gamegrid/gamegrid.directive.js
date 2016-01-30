(function () {
    angular.module('flaederGamesApp')
        .directive('fldrGameGrid', [function () {
            return {
                restrict: 'E',
                templateUrl: '/app/shared/gamegrid/gamegrid.template.html',
                controller: 'GameGridController'
            };
    }]);
})();
