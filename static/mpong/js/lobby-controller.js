(function () {

    angular.module('lobby', ['player', 'game', 'player-service'])
        .controller('LobbyController', ['$scope', 'playerService', function ($scope, playerService) {
            $scope.initialized = false;
            $scope.name = '';

            $scope.initialize = function () {
                playerService.getPlayer(function (result) {
                    if (result.data.player.name) {
                        $scope.name = result.data.player.name;
                        $scope.initialized = true;
                    }
                });
            };

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
