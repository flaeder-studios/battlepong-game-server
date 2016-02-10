(function () {

    angular.module('flaederGamesApp')
        .controller('HomeController', ['$scope', '$location', '$uibModal', 'playerService', function ($scope, $location, $uibModal, playerService) {

            $scope.isRegistered = false;
            $scope.player = undefined;
            $scope.changeName = false;

            $scope.initialize = function () {
                $scope.updatePlayerData(function (data) {
                    if ($scope.isRegistered) {
                        $location.path('/lobby');
                    } else {
                        $scope.openRegisterModal();
                    }
                });
            };

            $scope.openRegisterModal = function () {
                var modalInstance = $uibModal.open({
                    animation: true,
                    templateUrl: '/app/shared/register-modal/register-modal.template.html',
                    controller: 'RegisterModalController',
                });

                modalInstance.result.then(function (name) {
                    $scope.setPlayerName(name);
                }, function () {
                    console.log('Register modal dismissed at: ' + new Date());
                });

            };

            $scope.openSetNameModal = function () {
                var modalInstance = $uibModal.open({
                    animation: true,
                    templateUrl: '/app/shared/set-name-modal/set-name-modal.template.html',
                    controller: 'SetNameModalController',
                });

                modalInstance.result.then(function (name) {
                    $scope.setPlayerName(name);
                }, function () {
                    console.log('Set name modal dismissed at: ' + new Date());
                });

            };

            $scope.updatePlayerData = function (callback) {
                playerService.getPlayer(function (data) {
                    if (data.player) {
                        console.log('player is ', data.player);
                        $scope.player = data.player;
                        if ($scope.player.name) {
                            $scope.isRegistered = true;
                            $location.path('/lobby');
                        }
                        if (callback) {
                            callback(data.player);
                        }
                    }
                });
            };

            $scope.setPlayerName = function (name) {
                playerService.setName(name, function (data) {
                    $scope.player = data.player;
                    if (data.player.name == name) {
                        console.log("set player name to", $scope.player.name);
                        $scope.changeName = false;
                        $scope.isRegistered = true;
                        $location.path('/lobby');
                    } else {
                        alert('could not set name to ' + name);
                    }
                });
            };

            $scope.initialize();

            }]);

})();
