(function () {

    "use strict";

    angular.module('flaederGamesApp')
        .controller('BattlePongController', ['$scope', '$window', '$location', '$timeout','BattlePongService', 'lobbyService', 'playerService', 'gameService', function ($scope, $window, $location, $timeout, BattlePongService, lobbyService, playerService, gameService) {

            $scope.pTime = 0;
            $scope.gameState = {balls: {}, players: {}};
            $scope.gameOn = false;

            $scope.startGame = function () {
                console.log("starting game...");
                $scope.gameOn = true;
                BattlePongService.initGame();
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
                    $scope.gameState.paddles[0].refVelocity = [0.0, 1.0];
                } else if (e.keyCode == 40) { // down
                    $scope.gameState.paddles[0].refVelocity = [0.0, -1.0];
                }
            };

            $scope.handleKeyRelease = function (e) {
                if (e.keyCode == 38 || e.keyCode == 40) {
                    $scope.gameState.paddles[0].refVelocity = [0.0, 0.0];
                }
            };

            function setState (data) {
                for (var ball in data.balls) {
                    $scope.gameState.balls[ball].position = data.balls[ball].position;
                    $scope.gameState.balls[ball].radius = data.balls[ball].radius * 100.0;
                    $scope.gameState.balls[ball].velocity = [0.0,0.0];
                }
                for (var paddle in data.paddles) {
                    $scope.gameState.paddles[paddle].position = data.paddles[paddle].position;
                    $scope.gameState.paddles[paddle].velocity = [0.0,0.0];
                    $scope.gameState.paddles[paddle].width = data.paddles[paddle].dimensions[0];
                    $scope.gameState.paddles[paddle].height = data.paddles[paddle].dimensions[1];
                    $scope.gameState.paddles[paddle].score = data.paddles[paddle].score;
                }
            }

            function initState (data) {
                for (var ball in data.balls) {
                    $scope.gameState.balls[ball] = {};
                    $scope.gameState.balls[ball].position = data.balls[ball].position;
                    $scope.gameState.balls[ball].radius = data.balls[ball].radius;
                    $scope.gameState.balls[ball].velocity = [0.0,0.0];
                    $scope.gameState.balls[ball].color = [0.0, 0.0, 1.0, 1.0];
                }
                for (var paddle in data.players) {
                    $scope.gameState.players[paddle] = {};
                    $scope.gameState.players[paddle].position = data.players[paddle].position;
                    $scope.gameState.players[paddle].velocity = [0.0,0.0];
                    $scope.gameState.players[paddle].refVelocity = [0.0,0.0];
                    $scope.gameState.players[paddle].acceleration = [0.0,0.0];
                    $scope.gameState.players[paddle].width = data.players[paddle].dimensions[0];
                    $scope.gameState.players[paddle].height = data.players[paddle].dimensions[1];
                    $scope.gameState.players[paddle].color = [1.0, 0.0, 0.0, 1.0];
                    $scope.gameState.players[paddle].score = data.players[paddle].score;
                }
            }

            function updateState() {
                var i, ball, paddle;
                gameService.getState($scope.currentPlayer.currentGame.id, function (data) {
                    setState(data)
                    if ($scope.gameOn == true) {
                        $timeout(updateState, 2000);
                    }
                });
            }

            function startStuff() {
                playerService.getPlayer(function (data) {
                    $scope.currentPlayer = data.player;
                    gameService.getState($scope.currentPlayer.currentGame.id, function (data) {
                        $scope.gameOn = true;
                        initState(data);
                        render($scope.pTime);
                        updateState();
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
                    BattlePongService.handleWallBounce(ball);
                    for (paddle in $scope.gameState.paddles) {
                        paddle = $scope.gameState.paddles[paddle];
                        BattlePongService.handlePaddleBounce(ball, paddle);
                    }
                    BattlePongService.moveBall(ball, dt);
                    BattlePongService.drawBall(ball);
                }
                for (paddle in $scope.gameState.players) {
                    paddle = $scope.gameState.players[paddle];
                    BattlePongService.movePaddle(paddle, dt);
                    BattlePongService.drawPaddle(paddle);
                }
                if($scope.gameOn == true) {
                    $window.requestAnimationFrame(render);
                }
            };

            $scope.startGame();

    }]);
})();
