(function () {

    angular.module('flaederGamesApp')
        .controller('RegisterModalController', ['$scope', '$uibModalInstance', function ($scope, $uibModalInstance) {

            $scope.newName = '';

            $scope.register = function () {
                $uibModalInstance.close($scope.newName);
            }

            $scope.cancel = function () {
                $uibModalInstance.dismiss('cancel');
            }

        }]);

})();
