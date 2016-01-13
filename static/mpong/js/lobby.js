(function () {

    angular.module('lobby', ['player', 'game'])
        .controller('LobbyController', ['$scope', function ($scope) {
            $scope.name = '';
    }]);

})();
