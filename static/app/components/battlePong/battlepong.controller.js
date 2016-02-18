(function () {

    "use strict";

    angular.module('flaederGamesApp')
        .controller('BattlePongController', ['$scope', 'BattlePongService', function ($scope, BattlePongService) {

            $scope.gameState = undefined;

            BattlePongService.initGame('2d-vertex-shader', '2d-fragment-shader');
            BattlePongService.drawBall({
                position: 1
            });

    }]);
})();
