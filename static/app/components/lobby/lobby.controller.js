(function () {

    'use strict';

    angular.module('flaederGamesApp')
        .controller('LobbyController', ['$scope', '$location', 'lobbyService', function ($scope, $location, lobbyService) {

            $scope.currentGame = undefined;
            $scope.newGame = {};
            $scope.createGameFormActive = false;
            $scope.games = [];

            $scope.activateCreateGameForm = function () {
                $scope.createGameFormActive = true;
            };

            $scope.deactivateCreateGameForm = function () {
                $scope.createGameFormActive = false;
                $scope.newGame = {};
            };

            $scope.listGames = function () {
                return lobbyService.getAllGames(function (data) {
                    $scope.games = data.games;
                });
            };

            $scope.startGame = function () {
                if ($scope.currentGame) {
                    $location.path('/game');
                }
            };

            $scope.createGame = function (game) {
                lobbyService.createGame(game, function (data) {
                    $scope.games.push(data.games[0]);
                    $scope.deactivateCreateGameForm();
                    console.log('created game ' + data.games[0]);
                });
            };

            $scope.removeGame = function (game) {
                var idx, removedGame;

                lobbyService.removeGame(game, function (data) {
                    removedGame = data.games[0];

                    for (var i = 0; i < $scope.games.length; i++) {
                        if ($scope.games[i].id == removedGame.id) {
                            idx = i;
                            break;
                        }
                    }

                    if (idx > -1) {
                        $scope.games.splice(idx, 1);
                        if ($scope.currentGame && $scope.currentGame.id == removedGame.id) {
                            $scope.setCurrentGame(undefined);
                        }
                    }
                    console.log('removed game ' + data.games[0])
                });
            };

            $scope.joinGame = function (game) {
                if (!$scope.currentGame) {
                    lobbyService.joinGame(game, function (data) {
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
                    lobbyService.leaveGame(function (data) {
                        var leftGame = data.games[0];
                        for (var i = 0; i < $scope.games.length; i++) {
                            if ($scope.games[i].id === leftGame.id) {
                                $scope.games[i] = leftGame;
                                break;
                            }
                        }
                        $scope.setCurrentGame(undefined);
                        console.log("leftGame: ", leftGame);
                    });
                }
            };

            $scope.setCurrentGame = function (game) {
                $scope.currentGame = game;
                console.info("current game is ", $scope.currentGame);
            };

            $scope.getCurrentGame = function () {
                lobbyService.getCurrentGame(function (currentGame) {
                    console.log("current game is", currentGame);
                    $scope.currentGame = currentGame;
                });
            };

            if (!$scope.isRegistered) {
                //$location.path('/home');
            }

            $scope.listGames();
            $scope.getCurrentGame();

    }]);

})();
