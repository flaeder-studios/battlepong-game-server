(function () {

    angular.module('game-service', [])
        .factory('gameService', [function () {
            var service = {};

            service.games = [{
                "id": "myGame",
                "maxPlayers": 2,
                "joinedPlayers": ['Arvid'],
                "createdBy": 'Arvid',
                "removable": true
            }, {
                "id": "hisGame",
                "maxPlayers": 2,
                "joinedPlayers": ['Arvid', 'Sigrid'],
                "createdBy": 'Sigrid'
            }, {
                "id": "anyonesGame",
                "maxPlayers": 2,
                "joinedPlayers": ['Malin'],
                "createdBy": 'Malin'
            }];

            service.getAllGames = function () {
                return this.games;
            };

            service.createGame = function (gameId, maxPlayers) {
                var game = {
                    "id": gameId,
                    "maxPlayers": maxPlayers,
                    "joinedPlayers": [],
                    "createdBy": 'Arvid?',
                    "removable": true
                };
                this.games.push(game)
                console.log("created game", game)
            };

            service.removeGame = function (game) {
                var idx = -1;
                for (var i = 0; i < this.games.length; i++) {
                    if (this.games[i] == game) {
                        idx = i;
                        break;
                    }
                }
                if (idx > -1) {
                    this.games.splice(idx, 1);
                    console.log("removed game ", game.id);
                }
            };

            service.joinGame = function (game) {
                game.joinedPlayers.push('ahmed');
                console.log("joined ", game.id);
            };

            service.leaveGame = function (game) {
                var idx = -1;
                for (var i = 0; i < game.joinedPlayers.length; i++) {
                    if (game.joinedPlayers[i] === 'ahmed') {
                        idx = i;
                        break;
                    }
                }
                if (idx > -1) {
                    game.joinedPlayers.splice(idx, 1);
                    console.log("left ", game.id);
                }
            };

            return service;
    }]);

})();
