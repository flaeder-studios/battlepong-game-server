(function () {

    'use strict';

    angular.module('flaederGamesApp')
        .config(['$routeProvider', function ($routeProvider) {
            $routeProvider.when('/lobby', {
                templateUrl: '/app/components/lobby/lobby.view.html',
                controller: 'LobbyController',
                controllerAs: 'lobby'
            }).when('/game', {
                templateUrl: '/app/components/game/game.view.html',
                controller: 'GameController'
            }).when('/home', {
                templateUrl: '/app/components/home/home.view.html',
                controller: 'HomeController'
            }).otherwise({
                redirectTo: '/home'
            });
        }]);

})();
