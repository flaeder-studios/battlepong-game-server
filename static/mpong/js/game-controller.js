(function () {
    angular.module("game", ['game-service'])
        .controller('GameController', ['$scope', 'gameService', '$interval', function ($scope, gameService, $interval) {

            $scope.hasJoinedGame = false;
            $scope.currentGame = {};
            $scope.newGame = {};
            $scope.createGameFormActive = false;

            $scope.games = [];

            $scope.activateCreateGameForm = function () {
                $scope.createGameFormActive = true;
                $scope.newGame = {};
            };

            $scope.deactivateCreateGameForm = function () {
                $scope.createGameFormActive = false;
                $scope.newGame = {};
            };

            $scope.listGames = function () {
                return gameService.getAllGames(function (data) {
                    $scope.games = data.games;
                });
            };

            $scope.gameUpdateInterval = $interval($scope.listGames, 2000);

            $scope.createGame = function (game) {
                gameService.createGame(game.id, game.maxPlayers, function (data) {
                    $scope.games.push(data.games[0]);
                    $scope.deactivateCreateGameForm();
                    console.log('created game ' + data.games[0]);
                });
            };

            $scope.removeGame = function (game) {
                var idx, removedGame;

                if ($scope.currentGame != game) {
                    gameService.removeGame(game, function (data) {
                        $scope.currentGame = {};
                        $scope.hasJoinedGame = false;
                        removedGame = data.games[0]

                        for (var i = 0; i < $scope.games.length; i++) {
                            if ($scope.games[i].id == removedGame.id) {
                                idx = i;
                                break;
                            }
                        }

                        if (idx > -1) {
                            $scope.games.splice(idx, 1);
                        }
                        console.log('removed game ' + data.games[0])
                    });
                }
            };

            $scope.joinGame = function (game) {
                if (!$scope.hasJoinedGame) {
                    gameService.joinGame(game, function (data) {
                        var joinedGame = data.games[0],
                            idx = -1;

                        for (var i = 0; i < $scope.games.length; i++) {
                            if ($scope.games[i].id == joinedGame.id) {
                                idx = i;
                                break;
                            }
                        }

                        if (idx > -1) {
                            $scope.games[idx] = joinedGame;
                        } else {
                            $scope.games.push(joinedGame);
                        }

                        $scope.currentGame = joinedGame;
                        $scope.hasJoinedGame = true;

                        console.log('joined game ', joinedGame);

                    });
                }
            };

            $scope.leaveGame = function () {
                if ($scope.hasJoinedGame) {
                    console.log("entered leaveGame");
                    gameService.leaveGame(function (data) {
                        var leftGame = data.games[0];
                        console.log("leftGame: ", leftGame);
                        for (var i = 0; i < $scope.games.length; i++) {
                            if ($scope.games[i].id === leftGame.id) {
                                $scope.games[i] = leftGame;
                                break;
                            }
                        }
                        $scope.hasJoinedGame = false;
                        $scope.currentGame = undefined;
                    });
                }
            };
        }]);
})();
