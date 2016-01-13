(function () {
    angular.module('playerAPIModule', [])
        .factory('playerAPI', function () {

            var api = {};

            api.setName = function (name) {
                console.log("setName", name);
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
