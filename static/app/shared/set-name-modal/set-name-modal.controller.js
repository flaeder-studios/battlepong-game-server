(function () {

    angular.module('flaederGamesApp')
        .controller('SetNameModalController', ['$scope', '$uibModalInstance', function ($scope, $uibModalInstance) {

            $scope.newName = '';

            $scope.setName = function () {
                $uibModalInstance.close($scope.newName);
            }

            $scope.cancel = function () {
                $uibModalInstance.dismiss('cancel');
            }

        }]);

})();
