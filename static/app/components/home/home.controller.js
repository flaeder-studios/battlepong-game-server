(function () {

    angular.module('flaederGamesApp')
        .controller('HomeController', ['$scope', '$location', 'playerService', function ($scope, $location, playerService) {

            $scope.isRegistered = false;
            $scope.player = '';
            $scope.newName = '';
            $scope.changeName = false;

            $scope.initialize = function () {
                if ($scope.isRegistered) {
                    $location.path('/lobby')
                } else {
                    $scope.updatePlayerData();
                };
            };

            $scope.updatePlayerData = function () {
                playerService.getPlayer(function (data) {
                    if (data.player) {
                        console.log('player is ', data.player);
                        $scope.player = data.player;
                        if ($scope.player.name) {
                            $scope.isRegistered = true;
                        }
                    }
                });
            };

            $scope.setPlayerName = function (name) {
                playerService.setName(name, function (data) {
                    $scope.player = data.player;
                    if (data.player.name == name) {
                        console.log("Set player name to", $scope.playerName);
                        $scope.changeName = false;
                        if (!$scope.isRegistered) {
                            $scope.isRegistered = true;
                            $location.path('/lobby');
                        }
                    } else {
                        alert('could not set name to ' + name);
                    }
                });
            };

            $scope.initialize();

            }]);

})();
