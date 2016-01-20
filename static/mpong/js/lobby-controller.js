(function () {

    angular.module('lobby', ['player', 'game', 'player-service', 'ngRoute'])
        .config(['$routeProvider', function ($routeProvider) {
            $routeProvider.when('lobby', {

            });
        }])
        .controller('LobbyController', ['$scope', 'playerService', '$location', function ($scope, playerService, $location) {
            $scope.initialized = false;
            $scope.name = '';

            $scope.startSession = function (name) {
                playerService.setName(name, function (result) {
                    if (result.data.player.name) {
                        $scope.name = result.data.player.name;
                        $scope.initialized = true;
                    }
                });
            };

            $scope.setName = function (name) {
                $scope.name = name;
                console.log("setName", $scope.name);
            };

            $scope.initialize();

    }]);

})();
