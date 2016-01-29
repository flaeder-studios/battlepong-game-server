(function () {

    angular.module('flaederGamesApp')
        .controller('HomeController', ['$scope', '$location', 'playerService', function ($scope, $location, playerService) {

            $scope.isRegistered = false;
            $scope.playerName = '';
            $scope.newName = '';

            $scope.initialize = function () {
                if ($scope.isRegistered) {
                    $location.path('/lobby')
                } else {
                    playerService.getPlayer(function (data) {
                        if (data.player.name && data.player.name.length) {
                            $scope.playerName = data.player.name;
                            $scope.isRegistered = true;
                            $location.path('/lobby');
                        } else {
                            $scope.isRegistered = false;
                            $scope.playerName = '';
                        }
                    });
                }
            };

            $scope.registerPlayer = function (name) {
                playerService.setName(name, function (data) {
                    $scope.isRegistered = true;
                    $scope.playerName = data.player.name;
                    console.log("Set player name to", $scope.playerName);
                    $location.path('/lobby');
                });
            };

            $scope.setPlayerName = function (name) {
                if (name) {
                    $scope.playerName = name;
                }
            };

            $scope.initialize();

        }]);

})();
