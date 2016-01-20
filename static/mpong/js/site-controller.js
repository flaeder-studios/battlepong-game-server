(function () {

    "use strict";

    angular.module('site', ['ngRoute', 'player-service', 'register-controller', 'lobby', 'game-loader-controller'])
        .controller('SiteController', ['$scope', 'playerService', '$location', function ($scope, playerService, $location) {

            $scope.currentGame = undefined;
            $scope.playerName = undefined;
            $scope.isRegistered = false;

            $scope.setPlayerName = function (name) {
                $scope.playerName = name;
                $scope.isRegistered = true;
                console.info("set name to ", $scope.playerName);
            };

            $scope.setCurrentGame = function (game) {
                $scope.currentGame = game;
                console.info("current game is ", $scope.currentGame);
            };

            $scope.startGame = function (game) {
                console.info("starting game ", $scope.currentGame);
            };

            $scope.quitGame = function () {
                console.info("quit game ", $scope.currentGame);
            };

            $scope.gotoLobby = function () {
                console.info("quit game ", $scope.currentGame);
            };

            $scope.initialize = function () {
                playerService.getPlayer(function (result) {
                    var player = result.data.player;

                    if (player.name) {
                        $scope.playerName = player.name;
                        $scope.isRegistered = true;
                        console.log("registered as", $scope.playerName);
                    } else {
                        console.log("not registered")
                        $location.path('/register');
                    }

                    if (player.currentGame) {
                        $scope.currentGame = player.currentGame;
                        console.log("current game is", $scope.currentGame);
                    }

                });
            };

            $scope.initialize();

        }])
        .config(['$routeProvider', function ($routeProvider) {
            $routeProvider.when('/register', {
                templateUrl: 'register.html',
                controller: 'RegisterController'
            }).when('/lobby', {
                templateUrl: 'lobby.html',
                controller: 'LobbyController'
            }).when('/game/:gameName', {
                templateUrl: 'loading.html',
                controller: 'GameLoaderController'
            }).otherwise({
                redirectTo: '/lobby'
            });
        }]);

})();
