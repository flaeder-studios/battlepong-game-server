(function () {
    angular.module("game", ['game-service', 'ui.grid', 'ui.grid.selection'])
        .controller('GameController', ['$scope', '$location', 'gameService', '$interval', 'uiGridConstants', '$timeout', function ($scope, $location, gameService, $interval, uiGridConstants, $timeout) {

            $scope.newGame = {};
            $scope.createGameFormActive = false;

            $scope.games = [];
            $scope.selectedGame = undefined;

            $scope.gameGrid = {
                data: 'games',
                enableSorting: true,
                enableFiltering: true,
                enableRowSelection: true,
                multiSelect: false,
                enableRowHeaderSelection: false,
                enableSelectAll: false,

                onRegisterApi: function (gridApi) {
                    //set gridApi on scope
                    $scope.gridApi = gridApi;
                    gridApi.selection.on.rowSelectionChanged($scope, function (row) {
                        console.log('selected row', row);
                        $scope.selectedGame = row.entity;
                        row.isSelected = true;
                    });
                },

                columnDefs: [{
                    field: 'name',
                    name: 'name'
                }, {
                    field: 'id',
                    name: 'name'
                }, {
                    field: 'createdBy',
                    name: 'Created By'
                }, {
                    cellTemplate: "<span> {{ row.entity.joinedPlayers.length + ' / ' + row.entity.maxPlayers }} </span>",
                    name: "Joined / Max"
                }, {
                    cellTemplate: '/mpong/game-grid-control.html',
                    name: 'Joined Players',
                    enableSorting: false,
                    enableFiltering: false
                }],
            };

            $scope.updateGridSelection = function () {
                if ($scope.selectedGame) {
                    console.log('calling selectRow with', $scope.selectedGame);

                    if ($scope.selectedGame) {
                        $timeout(function () {
                            var idx = -1;

                            for (var i = 0; i < $scope.games.length; i++) {
                                if ($scope.games[i].id == $scope.selectedGame.id) {
                                    idx = i;
                                    break;
                                }
                            }

                            if (idx > -1) {
                                //$scope.gridApi.selection.selectRow($scope.selectedGame);
                                $scope.gridApi.selection.selectRow($scope.games[idx]);
                            } else {
                                $scope.selectedGame = undefined;
                            }
                        }, 100);
                    }
                }
            };

            $scope.activateCreateGameForm = function () {
                $scope.createGameFormActive = true;
            };

            $scope.deactivateCreateGameForm = function () {
                $scope.createGameFormActive = false;
                $scope.newGame = {};
            };

            $scope.listGames = function () {
                return gameService.getAllGames(function (data) {
                    $scope.games = data.games;
                    $scope.updateGridSelection();
                });
            };

            $scope.startGame = function () {
                if ($scope.currentGame) {
                    $location.path('/game/' + $scope.currentGame.name)
                }
            };

            $scope.createGame = function (game) {
                gameService.createGame(game, function (data) {
                    $scope.games.push(data.games[0]);
                    $scope.deactivateCreateGameForm();
                    console.log('created game ' + data.games[0]);
                });
            };

            $scope.removeGame = function (game) {
                var idx, removedGame;

                gameService.removeGame(game, function (data) {
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
                        $scope.updateGridSelection();
                        console.log('joined game ', joinedGame);

                    });
                }
            };

            $scope.leaveGame = function () {
                if ($scope.currentGame) {
                    gameService.leaveGame(function (data) {
                        var leftGame = data.games[0];
                        for (var i = 0; i < $scope.games.length; i++) {
                            if ($scope.games[i].id === leftGame.id) {
                                $scope.games[i] = leftGame;
                                break;
                            }
                        }
                        $scope.setCurrentGame(undefined);
                        $scope.updateGridSelection();
                        console.log("leftGame: ", leftGame);
                    });
                }
            };

            $scope.getCurrentGame = function () {
                return $scope.getCurrentGame;
            };

            if (!$scope.isRegistered) {
                $location.path('/register');
                console.log("going to /register")
            } else {
                $scope.listGames();
                //$scope.gameUpdateInterval = $interval($scope.listGames, 2000);
            }

}]);
})();
