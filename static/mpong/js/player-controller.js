(function () {

    angular.module('player', ['player-service'])
        .controller('PlayerController', ['$scope', 'playerService', function ($scope, playerService) {
            $scope.changeName = false;

            $scope.setName = function (name) {
                if (name) {
                    $scope.name = playerService.setName(name);
                    $scope.changeName = false;
                    console.log("setName", $scope.name);
                }
            };
        }]);

})();
