(function () {
    angular.module("game", [])
        .controller('GameController', ['$scope', function ($scope) {

            $scope.games = [{
                    "id": "myGame",
                    "maxPlayers": 2,
                    "joinedPlayers": ['Arvid'],
                    "createdBy": 'Arvid'
                }, {
                    "id": "hisGame",
                    "maxPlayers": 2,
                    "joinedPlayers": ['Arvid', 'Sigrid'],
                    "createdBy": 'Sigrid'
                },
                {
                    "id": "anyonesGame",
                    "maxPlayers": 2,
                    "joinedPlayers": ['Malin'],
                    "createdBy": 'Malin'
                }];

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

            $scope.createGame = function (game) {
                game.createdBy = 'daniel?';
                game.joinedPlayers = ['daniel?'];
                $scope.games.push(game);
                console.log("created game", game)
            };

            $scope.removeGame = function (game) {
                var idx = -1;
                for (var i = 0; i < $scope.games.length; i++) {
                    if ($scope.games[i] == game) {
                        idx = i;
                        break;
                    }
                }
                if (idx > -1) {
                    $scope.games.splice(idx, 1);
                    console.log("removed game ", game.id);
                }
            };

            $scope.joinGame = function (game) {
                if (!$scope.hasJoinedGame) {
                    $scope.currentGame = game;
                    $scope.hasJoinedGame = true;
                    console.log(player.name, " joined ", game.id);
                }
            };

            $scope.leaveGame = function (game) {
                if ($scope.hasJoinedGame) {
                    $scope.hasJoinedGame = false;
                    $scope.currentGame = {};
                    console.log(player.name, " left ", game.id);
                }
            };


        }])
})();
