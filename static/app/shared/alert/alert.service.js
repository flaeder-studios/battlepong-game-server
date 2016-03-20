(function () {

    "use strict";

    angular.module('flaederGamesApp')
        .factory('alertService', ['$http', '$location', function ($http, $location) {

            var service = {};

            service.alerts = [];

            service.displayAlert = function(type, message) {
                this.alerts.push({type: type, message: message});
            };
             
            service.closeAlert = function(index) {
                this.alerts.splice(index, 1);
            };

            return service;

        }]);

})();
