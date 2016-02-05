(function () {

    'use strict';

    angular.module('flaederGamesApp')
        .controller('LobbyController', ['$scope', '$location', 'lobbyService', function ($scope, $location, lobbyService) {

            $scope.newGame = {};
            $scope.games = [];
            $scope.selectionState = undefined;
            $scope.createGameFormActive = false;

            $scope.cancelCreateGameForm = function () {
                $scope.createGameFormActive = false;
                $scope.newGame = {};
            };

            $scope.activateCreateGameForm = function () {
                $scope.createGameFormActive = true;
                $scope.newGame = {};
            };

            $scope.listGames = function () {
                return lobbyService.getAllGames(function (data) {
                    $scope.games = data.games;
                });
            };

            $scope.startGame = function () {
                if ($scope.player.currentGame) {
                    $location.path('/game');
                }
            };

            $scope.createGame = function (game) {
                lobbyService.createGame(game, function (data) {
                    $scope.games.push(data.games[0]);
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
                        if ($scope.player.currentGame && $scope.player.currentGame.id == removedGame.id) {
                            $scope.updatePlayerData();
                        }
                    }
                    console.log('removed game ' + data.games[0])
                });
            };

            $scope.joinGame = function (game) {
                if (!$scope.player.currentGame) {
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

                        $scope.updatePlayerData();

                        console.log('joined game ', joinedGame);
                    });
                }
            };

            $scope.leaveGame = function () {
                if ($scope.player.currentGame) {
                    lobbyService.leaveGame(function (data) {
                        var leftGame = data.games[0];
                        for (var i = 0; i < $scope.games.length; i++) {
                            if ($scope.games[i].id === leftGame.id) {
                                $scope.games[i] = leftGame;
                                break;
                            }
                        }
                        $scope.updatePlayerData();
                        console.log("leftGame: ", leftGame);
                    });
                }
            };

            $scope.selectedGame = undefined;

            $scope.gameGrid = {
                data: 'games',
                enableSorting: true,
                enableFiltering: true,
                enableRowSelection: true,
                multiSelect: false,
                enableRowHeaderSelection: false,
                enableSelectAll: false,
                rowTemplate: '/app/shared/gamegrid/game-grid-row.html',
                enableColumnMenus: false,

                onRegisterApi: function (gridApi) {
                    //set gridApi on scope
                    $scope.gridApi = gridApi;
                    console.log("onRegisterApi")
                },

                columnDefs: [{
                    cellTemplate: '/app/shared/gamegrid/game-grid-control.html',
                    name: 'Control',
                    enableHiding: false,
                    enableSorting: false,
                    suppressRemoveSort: true,
                }, {
                    field: 'name',
                    name: 'name',
                    suppressRemoveSort: true,
                    enableHiding: false
                }, {
                    field: 'id',
                    name: 'name',
                    suppressRemoveSort: true,
                    enableHiding: false
                }, {
                    field: 'createdBy',
                    name: 'Created By',
                    suppressRemoveSort: true,
                    enableHiding: false
                }, {
                    cellTemplate: "<span> {{ row.entity.joinedPlayers.length + ' / ' + row.entity.maxPlayers }} </span>",
                    name: "Joined / Max",
                    suppressRemoveSort: true,
                    enableHiding: false,
                    sortingAlgorithm: function (a, b, rowA, rowB, direction) {
                        var aFullPercent = rowA.entity.joinedPlayers.length / rowA.entity.maxPlayers,
                            bFullPercent = rowB.entity.joinedPlayers.length / rowB.entity.maxPlayers;
                        if (Math.abs(aFullPercent - bFullPercent) < 0.00001) {
                            if (rowB.entity.maxPlayers == rowA.entity.maxPlayers) {
                                return 0;
                            } else if (rowB.entity.maxPlayers < rowA.entity.maxPlayers) {
                                return 1;
                            } else {
                                return -1;
                            }
                        } else if (aFullPercent > bFullPercent) {
                            return 1;
                        } else {
                            return -1;
                        }
                    }
                }, {
                    cellTemplate: '<span ng-repeat="name in row.entity.joinedPlayers"> {{ name }} </span>',
                    name: 'Joined Players',
                    sortingAlgorithm: function (a, b, rowA, rowB, direction) {
                        a = rowA.entity.joinedPlayers.length;
                        b = rowB.entity.joinedPlayers.length;
                        if (a > b) {
                            return -1;
                        } else if (a < b) {
                            return 1;
                        } else {
                            return 0;
                        }
                    }
                }]
            };

            if (!$scope.isRegistered) {
                $location.path('/home');
            }

            $scope.listGames();

            }]);

})();
