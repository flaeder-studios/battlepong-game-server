(function () {
    angular.module('player-service', [])
        .factory('playerService', function () {

            var api = {};

            api.setName = function (name) {
                if (name) {
                    return name;
                }
            };


            api.getPlayer = function () {
                return {
                    name: 'daniel'
                };
            };

            return api;

        });
})();
