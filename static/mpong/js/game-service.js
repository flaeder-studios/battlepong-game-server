(function () {

    angular.module('game-service', ['http-method-service', 'url-service'])
        .factory('gameService', ['httpMethodService', 'urlService', function (httpMethodService, urlService) {
            var service = {};

            service.getAllGames = function (callback) {
                httpMethodService.get(urlService.gameUri, {}, function (result) {
                    callback(result.data);
                });
            };

            service.createGame = function (gameId, maxPlayers, callback) {
                var game = {
                    "id": gameId,
                    "maxPlayers": maxPlayers
                };

                httpMethodService.post(urlService.gameUri + '/' + gameId, game, {}, function (result) {
                    callback(result.data);
                });
            };

            service.removeGame = function (game, callback) {
                httpMethodService.delete(urlService.gameUri + '/' + game.id, {}, function (result) {
                    callback(result.data);
                });
            };

            service.joinGame = function (game, callback) {
                httpMethodService.post(urlService.joinUri + '/' + game.id, {}, {}, function (result) {
                    callback(result.data);
                });
            };

            service.leaveGame = function (callback) {
                httpMethodService.post(urlService.leaveUri, {}, {}, function (result) {
                    callback(result.data);
                });
            };

            return service;
    }]);

})();
