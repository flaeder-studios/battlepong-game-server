(function () {
    angular.module('flaederGamesApp')
        .factory('gameService', ['httpMethodService', 'urlService', function (httpMethodService, urlService) {
            service = {};

            service.startGame = function (callback) {
                httpMethodService.post(urlService.startUri, {}, {}, function (result) {
                    callback(result.data);
                });
            };

            service.getState = function (gameId, callback) {
                httpMethodService.get(urlService.stateUri + '/' + gameId, {id: gameId}, function (result) {
                    callback(result.data);
                });
            };

            service.quitGame = function (callback) {
                httpMethodService.post(urlService.quitUri, {}, {}, function (result) {
                    callback(result.data);
                });
            };

            return service;
    }]);
})();
