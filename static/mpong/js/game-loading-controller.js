(function () {
    angular.module('game-loader-controller', ['angularLoad'])
        .controller('GameLoaderController', ['$scope', '$routeParams', '$location', 'angularLoad', function ($scope, $routeParams, $location, angularLoad) {

            $scope.startCurrentGame = function () {
                console.log("launching current game", $routeParams.gameName);
                if ($scope.nLoadedFiles == $scope.nFilesToLoad) {
                    window.location.assign($scope.currentGame.template);
                }
            };

            $scope.loadCurrentGame = function () {
                console.log('loading current game')
                var game = $scope.currentGame;
                console.log("game:", game)
                if (game) {
                    $scope.nLoadedFiles = 0;
                    $scope.nFilesToLoad = game.scripts.length;
                    for (var i = 0; i < game.scripts.length; i++) {
                        console.log('attempting load of', game.scripts[i])
                        angularLoad.loadScript(game.scripts[i]).then(function () {
                            console.log('load successful!');
                            $scope.nLoadedFiles += 1;
                        }).catch(function () {
                            console.error('could not load file');
                            $location.path('/lobby');
                        });
                    }
                }
            };

            $scope.exitCurrentGame = function () {

            };

            if (!$scope.isRegistered) {
                $location.path('/register');
            }

            if ($scope.currentGame) {
                $scope.loadCurrentGame();
            } else {
                $location.path('/lobby');
            }

        }]);

})();
