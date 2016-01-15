(function () {
    angular.module('http-method-service', [])
        .factory('httpMethodService', ['$http', function ($http) {

            var service = {};

            service.get = function (uri, config, callback) {
                var res = {};

                $http.get(uri, config).then(
                    function (result) {
                        callback(result);
                    },
                    function (rejectReason) {
                        console.error(rejectReason);
                    });
            };

            service.post = function (uri, data, config, callback) {
                var res = {};

                $http.post(uri, data, config).then(
                    function (result) {
                        callback(result);
                    },
                    function (rejectReason) {
                        console.error(rejectReason);
                    });
            };

            service.delete = function (uri, config, callback) {
                var res = {};

                $http.delete(uri, config).then(
                    function (result) {
                        callback(result);
                    },
                    function (rejectReason) {
                        console.error(rejectReason);
                    });
            };

            return service;

        }]);
})();
