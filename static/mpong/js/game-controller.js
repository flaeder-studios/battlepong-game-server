(function () {
    angular.module("game", ['game-service'])
        .controller('GameController', ['$scope', '$location', 'gameService', '$interval', function ($scope, $location, gameService, $interval) {

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

            $scope.startGame = function () {
                if ($scope.currentGame) {
                    $location.path('/game/' + $scope.currentGame.name)
                }
            };

            $scope.createGame = function (game) {
                gameService.createGame(game.id, game.maxPlayers, function (data) {
                    $scope.games.push(data.games[0]);
                    $scope.deactivateCreateGameForm();
                    console.log('created game ' + data.games[0]);
                });
            };

            $scope.removeGame = function (game) {
                var idx, removedGame;

                gameService.removeGame(game, function (data) {
                    removedGame = data.games[0]

                    for (var i = 0; i < $scope.games.length; i++) {
                        if ($scope.games[i].id == removedGame.id) {
                            idx = i;
                            break;
                        }
                    }

                    if (idx > -1) {
                        $scope.games.splice(idx, 1);
                        if ($scope.currentGame == removedGame) {
                            $scope.setCurrentGame(undefined);
                        }
                    }
                    console.log('removed game ' + data.games[0])
                });

            };

            $scope.joinGame = function (game) {
                if (!$scope.currentGame) {
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

                        $scope.setCurrentGame(joinedGame);

                        console.log('joined game ', joinedGame);

                    });
                }
            };

            $scope.leaveGame = function () {
                if ($scope.currentGame) {
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
                        $scope.setCurrentGame(undefined);
                    });
                }
            };

            if (!$scope.isRegistered) {
                $location.path('/register');
                console.log("going to /register")
            } else {
                $scope.listGames();
                $scope.gameUpdateInterval = $interval($scope.listGames, 2000);
            }

        }]);
})();
