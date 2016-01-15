(function () {
    angular.module('player-service', ['http-method-service', 'url-service'])
        .factory('playerService', ['httpMethodService', 'urlService', function (httpMethodService, urlService) {

            var service = {};

            service.setName = function (name, callback) {
                if (name) {
                    var data = {}
                    data.player = {};
                    data.player.name = name;
                    httpMethodService.post(urlService.playerUri, data, {}, callback);
                }
            };

            service.getPlayer = function (callback) {
                httpMethodService.get(urlService.playerUri, {}, callback);
            };

            return service;

        }]);
})();
