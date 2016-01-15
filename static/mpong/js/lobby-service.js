(function () {
    angular.module('lobby-service', ['player-service'])
        .factory('lobbyService', ['playerService', function (playerService) {
            service = {};

            return service;
    }]);
})();
