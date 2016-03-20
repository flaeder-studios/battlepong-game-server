(function () {
    angular.module('flaederGamesApp')
        .factory('httpMethodService', ['$http', '$location', function ($http, $location) {

            var service = {};

            var defaultErrorHandler = function (rejectReason) {
                if (rejectReason.status == 401) {
                    //$location.path('/register');
                } else {
                    console.error(rejectReason);
                }
            };

            service.get = function (uri, config, callback, errorhandler) {
                var res = {};

                $http.get(uri, config).then(
                    function (result) {
                        callback(result);
                    },
                    function (rejectReason) {
                        errorhandler(rejectReason);
                    });
            };

            service.post = function (uri, data, config, callback, errorhandler) {
                var res = {};

                $http.post(uri, data, config).then(
                    function (result) {
                        callback(result);
                    },
                    function (rejectReason) {
                        errorhandler(rejectReason);
                    });
            };

            service.delete = function (uri, config, callback, errorhandler) {
                var res = {};

                $http.delete(uri, config).then(
                    function (result) {
                        callback(result);
                    },
                    function (rejectReason) {
                        errorhandler(rejectReason);
                    });
            };

            return service;

        }]);
})();
