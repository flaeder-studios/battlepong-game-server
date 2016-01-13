(function () {
    angular.module('lobby-service', [])
        .factory('lobbyService', [function () {
            service = {};

            service.initSession = function (name) {
                return name;
            };

            return service;
    }]);
})();
