(function () {

    angular.module('player', [])
        .controller('PlayerController', ['$scope', function ($scope) {
            $scope.name = '';
            $scope.changeName = true;

            $scope.setName = function (name) {
                console.log("setName", name);
                if (name) {
                    $scope.name = name;
                    $scope.changeName = false;
                }
            };
        }]);

})();
