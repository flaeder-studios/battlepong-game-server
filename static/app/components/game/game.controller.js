(function () {

    angular.module("flaederGamesApp")
        .controller('GameController', ['$scope', '$location', 'gameService', 'playerService', 'lobbyService', function ($scope, $location, gameService, playerService, lobbyService) {

            $scope.initialize = function () {
                playerService.getPlayer(function (data) {
                    if (!data.player.currentGame) {
                       // $scope.backToLobby();
                    }
                });
            };

            $scope.startCurrentGame = function () {
                gameService.startGame(function (data) {
                    $scope.updatePlayerData(function (data) {
                        console.log("Starting game!");
                        $scope.$broadcast('startGameEvent');
                    });
                });
            };

            $scope.quitGame = function () {
                gameService.quitGame(function (data) {
                    $scope.updatePlayerData( function () {
                        $scope.$broadcast('quitEvent');
                    });
                });
            };

            $scope.backToLobby = function () {
                $location.path("/lobby");
            }

            $scope.initialize();

    }]);

})();
