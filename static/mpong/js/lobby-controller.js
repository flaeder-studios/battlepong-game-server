(function () {

    angular.module('lobby', ['player', 'game', 'lobby-service'])
        .controller('LobbyController', ['$scope', 'lobbyService', function ($scope, lobbyService) {
            $scope.initialized = false;
            $scope.name = '';

            $scope.initialize = function (name) {
                $scope.name = lobbyService.initSession(name);
                if (name === $scope.name) {
                    $scope.initialized = true;
                }
            };
    }]);

})();
