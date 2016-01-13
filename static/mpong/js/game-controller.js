(function () {
    angular.module("game", ['game-service'])
        .controller('GameController', ['$scope', 'gameService', function ($scope, gameService) {


            $scope.hasJoinedGame = false;
            $scope.currentGame = {};
            $scope.newGame = {};
            $scope.createGameFormActive = false;

            $scope.activateCreateGameForm = function () {
                $scope.createGameFormActive = true;
                $scope.newGame = {};
            };

            $scope.deactivateCreateGameForm = function () {
                $scope.createGameFormActive = false;
                $scope.newGame = {};
            };

            $scope.listGames = function () {
                return gameService.getAllGames();
            };

            $scope.createGame = function (game) {
                gameService.createGame(game.id, game.maxPlayers);
                $scope.deactivateCreateGameForm();
            };

            $scope.removeGame = function (game) {
                if (!$scope.hasJoinedGame) {
                    gameService.removeGame(game);
                    $scope.currentGame = {};
                    $scope.hasJoinedGame = false;
                }
            };

            $scope.joinGame = function (game) {
                if (!$scope.hasJoinedGame) {
                    gameService.joinGame(game);
                    $scope.currentGame = game;
                    $scope.hasJoinedGame = true;
                }
            };

            $scope.leaveGame = function (game) {
                if ($scope.hasJoinedGame) {
                    gameService.leaveGame(game);
                    $scope.hasJoinedGame = false;
                    $scope.currentGame = {};
                }
            };


        }])
})();
