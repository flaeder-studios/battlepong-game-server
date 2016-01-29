(function () {

    angular.module("flaederGamesApp")
        .controller('GameGridController', ['$scope', 'uiGridConstants', function ($scope, uiGridConstants) {

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
                },

                columnDefs: [{
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
                    cellTemplate: '/app/shared/gamegrid/game-grid-control.html',
                    name: 'Joined Players',
                    enableHiding: false,
                    enableSorting: true,
                    suppressRemoveSort: true,
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
                }],
            };

            $scope.rowHover = function (row) {
                row.isSelected ? row.isSelected = false : row.isSelected = true;
            };

            $scope.rowClick = function (row) {
                row.isSelected ? row.isSelected = false : row.isSelected = true;
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
                        }, 1);
                    }
                }
            };

        }]);

})();
