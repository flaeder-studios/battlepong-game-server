(function () {

    "use strict";

    angular.module('flaederGamesApp')
        .controller('BattlePongController', ['$scope', '$window', 'BattlePongService', function ($scope, $window, BattlePongService) {

            $scope.gameState = {
                balls: [],

                paddles: [{
                    color: [1.0, 0.0, 0.0, 1.0],
                    width: 0.01,
                    height: 0.1,
                    position: [0.5, 0.5],
                    velocity: [0.5, 0.4],
                }]
            };

            for (var i = 0; i < 100; ++i) {
                $scope.gameState.balls.push({
                    color: [Math.random(), Math.random(), Math.random(), 1.0],
                    radius: Math.random() * 0.05 + 0.05,
                    position: [Math.random() * 1.5 - 0.75, Math.random() * 1.5 - 0.75],
                    velocity: [Math.random() * 0.5 - 1, Math.random() * 0.5 - 1]
                });
            }

            function render(time) {
                $window.requestAnimationFrame(render);
                var i, ii, paddle, ball, dt;
                if ($scope.pTime === 0) {
                    dt = 0;
                } else {
                    dt = (time - $scope.pTime) / 1000
                }
                $scope.pTime = time;
                for (i = 0; i < $scope.gameState.balls.length; ++i) {
                    ball = $scope.gameState.balls[i];
                    BattlePongService.handleWallBounce(ball);
                    for (ii = 0; ii < $scope.gameState.paddles.length; ++ii) {
                        paddle = $scope.gameState.paddles[ii];
                        //BattlePongService.handlePaddleBounce(ball, paddle);
                    }
                    BattlePongService.moveBall(ball, dt);
                    BattlePongService.drawBall(ball);
                }

                for (i = 0; i < $scope.gameState.paddles.length; ++i) {
                    paddle = $scope.gameState.paddles[i];
                    BattlePongService.drawPaddle(paddle);
                }

            };

            BattlePongService.initGame('2d-vertex-shader', '2d-fragment-shader');
            var time = new Date();
            $scope.pTime = 0;
            render($scope.pTime);

    }]);
})();
