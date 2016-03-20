(function () {

    "use strict";

    angular.module('flaederGamesApp')
        .controller('BattlePongController', ['$scope', '$window', '$location', '$timeout','battlePongService', 'lobbyService', 'playerService', 'gameService', function ($scope, $window, $location, $timeout, battlePongService, lobbyService, playerService, gameService) {

            $scope.pTime = 0;
            $scope.pPaddleUpdate = 0;
            $scope.gameState = {balls: {}, players: {}};
            $scope.gameOn = false;

            $scope.startGame = function () {
                console.log("starting game...");
                $scope.gameOn = true;
                battlePongService.initGame();
                window.addEventListener('keydown', $scope.handleKeyPress, false);
                window.addEventListener('keyup', $scope.handleKeyRelease, false);
                startStuff();
            };

            $scope.quitGame = function () {
                gameService.quitGame(function (data) {
                    $scope.updatePlayerData( function () {
                        $scope.gameOn = false;
                        $location.path('/lobby');
                    });
                });
            };

            $scope.handleKeyPress = function (e) {
                if (e.keyCode == 38) { // up
                    $scope.gameState.players[$scope.player.name].refVelocity = [0.0, 1.0];
                } else if (e.keyCode == 40) { // down
                    $scope.gameState.players[$scope.player.name].refVelocity = [0.0, -1.0];
                }
            };

            $scope.handleKeyRelease = function (e) {
                console.log("handleKeyRelease");
                if (e.keyCode == 38 || e.keyCode == 40) {
                    $scope.gameState.players[$scope.player.name].refVelocity = [0.0, 0.0];
                }
            };

            function transformToCanvasCoord(pos) {
                return [pos[0], pos[1] / 0.625];
            }

            function setState (data) {
                for (var ball in data.balls) {
                    $scope.gameState.balls[ball].position = transformToCanvasCoord(data.balls[ball].position);
                    $scope.gameState.balls[ball].radius = data.balls[ball].radius;
                }
                for (var paddle in data.players) {
                    $scope.gameState.players[paddle].position = transformToCanvasCoord(data.players[paddle].position);
                    data.players[paddle].dimensions = transformToCanvasCoord(data.players[paddle].dimensions);
                    $scope.gameState.players[paddle].width = data.players[paddle].dimensions[0];
                    $scope.gameState.players[paddle].height = data.players[paddle].dimensions[1];
                    $scope.gameState.players[paddle].score = data.players[paddle].score;
                }
            }

            function initState (data) {
                for (var ball in data.balls) {
                    $scope.gameState.balls[ball] = {};
                    $scope.gameState.balls[ball].position = transformToCanvasCoord(data.balls[ball].position);
                    $scope.gameState.balls[ball].radius = data.balls[ball].radius;
                    $scope.gameState.balls[ball].velocity = [0.0,0.0];
                    $scope.gameState.balls[ball].color = [0.0, 0.0, 1.0, 1.0];
                }
                for (var paddle in data.players) {
                    $scope.gameState.players[paddle] = {};
                    $scope.gameState.players[paddle].position = transformToCanvasCoord(data.players[paddle].position);
                    $scope.gameState.players[paddle].velocity = [0.0,0.0];
                    $scope.gameState.players[paddle].refVelocity = [0.0,0.0];
                    $scope.gameState.players[paddle].acceleration = [0.0,2.0];
                    data.players[paddle].dimensions = transformToCanvasCoord(data.players[paddle].dimensions);
                    $scope.gameState.players[paddle].width = data.players[paddle].dimensions[0];
                    $scope.gameState.players[paddle].height = data.players[paddle].dimensions[1];
                    $scope.gameState.players[paddle].color = [1.0, 0.0, 0.0, 1.0];
                    $scope.gameState.players[paddle].score = data.players[paddle].score;
                }
            }

            function updatePaddleSpeed(paddle) {
                battlePongService.setPaddleSpeed(paddle.velocity[1], function() {
                    var dt = 0,
                        time = new Date().getTime();
                    if ($scope.gameOn) {
                        if ($scope.pPaddleUpdate === 0) {
                            $scope.pPaddleUpdate = time;
                        }
                        dt = (time - $scope.pPaddleUpdate) / 1000.0;
                        paddle.velocity[1] += (paddle.refVelocity[1] - paddle.velocity[1]) * paddle.acceleration[1] * dt;
                        if (Math.abs(paddle.velocity[1]) > Math.abs(paddle.refVelocity[1])) {
                            paddle.velocity[1] = paddle.refVelocity[1];
                        }
                        $scope.pPaddleUpdate = time;
                        updatePaddleSpeed(paddle);
                    }
                });
            }

            function updateState() {
                battlePongService.getState($scope.currentPlayer.currentGame.id, function (data) {
                    setState(data);
                    if ($scope.gameOn == true) {
                        updateState();
                    }
                });
            }

            function startStuff() {
                playerService.getPlayer(function (data) {
                    $scope.currentPlayer = data.player;
                    battlePongService.getState($scope.currentPlayer.currentGame.id, function (data) {
                        $scope.gameOn = true;
                        initState(data);
                        render($scope.pTime);
                        updateState();
                        updatePaddleSpeed($scope.gameState.players[$scope.player.name]);
                    });
                });
            }

            function render(time) {
                var i, ii, paddle, ball, dt;
                if ($scope.pTime === 0) {
                    dt = 0;
                } else {
                    dt = (time - $scope.pTime) / 1000
                }
                $scope.pTime = time;
                for (ball in $scope.gameState.balls) {
                    ball = $scope.gameState.balls[ball];
                    battlePongService.handleWallBounce(ball);
                    for (paddle in $scope.gameState.paddles) {
                        paddle = $scope.gameState.paddles[paddle];
                        battlePongService.handlePaddleBounce(ball, paddle);
                    }
                    battlePongService.moveBall(ball, dt);
                    battlePongService.drawBall(ball);
                }
                for (paddle in $scope.gameState.players) {
                    paddle = $scope.gameState.players[paddle];
                    battlePongService.movePaddle(paddle, dt);
                    battlePongService.drawPaddle(paddle);
                }
                if($scope.gameOn == true) {
                    $window.requestAnimationFrame(render);
                }
            };

            $scope.startGame();

    }]);
})();
