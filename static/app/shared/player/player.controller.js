(function () {

    angular.module('flaederGamesApp')
        .controller('PlayerController', ['$scope', '$location', 'playerService', function ($scope, $location, playerService) {
            $scope.changeName = false;

            $scope.getName = function () {
                $scope.name = playerService.getPlayer(function (data) {
                    $scope.setPlayerName(data.player.name);
                });
            };

            $scope.updateName = function (name) {
                if (name) {
                    $scope.name = playerService.setName(name, function (data) {
                        $scope.changeName = false;
                        $scope.setPlayerName(data.player.name);
                    });
                }
            };

            $scope.initialize = function () {
                $scope.getName(function (data) {
                    console.log("$scope.initialize", data)
                    if (data.player.name.length) {
                        $scope.name = data.player.name;
                    } else {
                        $location.path('/home');
                    }
                })
            };

            $scope.initialize();

            }]);

})();
