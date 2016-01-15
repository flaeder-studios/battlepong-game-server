(function () {

    angular.module('player', ['player-service'])
        .controller('PlayerController', ['$scope', 'playerService', function ($scope, playerService) {
            $scope.changeName = false;

            $scope.getName = function () {
                $scope.name = playerService.getName(name, function (result) {
                    $scope.name = result.data.player.name;
                    console.log("getName", $scope.name);
                });
            };

            $scope.updateName = function (name) {
                if (name) {
                    $scope.name = playerService.setName(name, function (result) {
                        $scope.changeName = false;
                        $scope.setName(result.data.player.name);
                    });
                }
            };
        }]);

})();
