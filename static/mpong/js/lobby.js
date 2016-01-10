(function () {

    var app = angular.module('lobby', []);

    app.controller('GameController', function () {
        this.games = games;
        this.currentGame = {};

        this.createGame = function (game, player) {
            game.createdBy = player.name;
            game.joinedPlayers = [];
            this.games.push(game);
            console.log("created game", game)
        };

        this.removeGame = function (game) {
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

        this.joinGame = function (game, player) {
            if (!this.currentGame) {
                this.currentGame = game;
                game.joinedPlayers.push(player.name);
                console.log(player.name, " joined ", game.id);
            }
        };

        this.leaveGame = function (player) {
            if (this.currentGame) {
                var idx = this.currentGame.joinedPlayers.indexOf(player);
                if (idx > -1) {
                    this.currentGame.joinedPlayers.splice(idx, 1);
                }
                this.currentGame = {};
                console.log(player.name, " left ", game.id);
            }
        };

    });

    app.controller('CreateGameController', function () {
        this.game = {};
        this.formActive = false;

        this.activateForm = function () {
            this.formActive = true;
        };

        this.deactivateForm = function () {
            this.formActive = false;
        };

        this.clearForm = function () {
            this.game = {};
        };
    });

    app.controller('PlayerController', function () {
        this.name = '';
        this.changeName = true;

        this.setName = function (name) {
            console.log("setName", name);
            if (name) {
                this.name = name;
                this.changeName = false;
            }
        };

    });

    var games = [
        {
            "id": "myGame",
            "maxPlayers": 2,
            "joinedPlayers": ['Arvid'],
            "createdBy": 'Arvid'
        },
        {
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
        }
    ];

})();
