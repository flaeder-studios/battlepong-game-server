(function () {

    angular.module("flaederGamesApp")
        .controller('GameController', ['$scope', '$location', 'playerService', 'lobbyService', function ($scope, $location, playerService, lobbyService) {

            $scope.currentGame = undefined;

            $scope.initialize = function () {
                playerService.getPlayer(function (data) {
                    if (data.player.currentGame) {
                        $scope.currentGame = data.player.currentGame;
                    } else {
                        $location.path("/lobby");
                    }
                });
            };

            $scope.quitGame = function () {
                if ($scope.currentGame) {
                    lobbyService.leaveGame(function (data) {
                        $location.path("/lobby");
                    });
                }
            };

            $scope.initialize();

    }]);

})();
