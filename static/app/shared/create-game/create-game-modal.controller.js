(function () {

    angular.module('flaederGamesApp')
        .controller('CreateGameModalController', ['$scope', '$uibModalInstance', 'doCreateGame', function ($scope, $uibModalInstance, doCreateGame) {

            $scope.newGame = {};
            $scope.doCreateGame = doCreateGame;

            $scope.createGame = function () {
                $scope.doCreateGame($scope.newGame, function () {
                    $uibModalInstance.close($scope.newGame);
                });
            }

            $scope.cancel = function () {
                $uibModalInstance.dismiss('cancel');
            }

        }]);

})();
