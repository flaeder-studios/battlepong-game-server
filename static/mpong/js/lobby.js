(function () {

    angular.module('lobby', ['player', 'game'])
        .controller('LobbyController', ['$scope', function ($scope) {
            $scope.initialized = false;

            $scope.initialize = function (name) {
                if (name) {
                    $scope.initialized = true;
                }
            };
    }]);

})();
