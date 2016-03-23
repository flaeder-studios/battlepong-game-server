(function () {

    "use strict";

    angular.module('flaederGamesApp')
        .controller('BattlePongController', ['$scope', '$window', '$location', '$timeout','BattlePongService', 'lobbyService', 'playerService', 'gameService', function ($scope, $window, $location, $timeout, BattlePongService, lobbyService, playerService, gameService) {

            $scope.pTime = 0;
            $scope.pPaddleUpdate = 0;
            $scope.gameState = {balls: {}, players: {}};
            $scope.gameOn = false;

            $scope.scoreBoardStyle = {}
            
            function componentToHex(c) {
                var hex = c.toString(16);
                return hex.length == 1 ? "0" + hex : hex;
            }

            function rgbToHex(r, g, b) {
                return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
            }

            function rgbArrayToHex(rgb) {
                return rgbToHex(rgb[0]*255|0, rgb[1]*255|0, rgb[2]*255|0);
            }

            $scope.resize = function (width, height) {
                $scope.width = width;
                $scope.height = height;
                $scope.updateStyle();
            };

            $scope.updateStyle = function () {
                for (var paddle in $scope.gameState.players) {
                    $scope.gameState.players[paddle].style = {
                        'color': rgbArrayToHex($scope.gameState.players[paddle].color),
                        'opacity': '0.6',
                        'font-size': '24px',
                        'position': 'relative',
                        'left': ($scope.width + 10).toString() + 'px'
                    };
                }
            };

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
                if ($scope.gameState.players[$scope.player.name]) {                
                    if (e.keyCode == 38) { // up
                        $scope.gameState.players[$scope.player.name].refVelocity = [0.0, 1.0];
                    } else if (e.keyCode == 40) { // down
                        $scope.gameState.players[$scope.player.name].refVelocity = [0.0, -1.0];
                    }
                }
            };

            $scope.handleKeyRelease = function (e) {
                if ($scope.gameState.players[$scope.player.name] && (e.keyCode == 38 || e.keyCode == 40)) {
                    $scope.gameState.players[$scope.player.name].refVelocity = [0.0, 0.0];
                }
            };

            function transformToCanvasCoord(pos) {
                return [pos[0], pos[1] / 0.618033];
            }

            function setState (data) {
                for (var ball in data.balls) {
                    $scope.gameState.balls[ball].position = transformToCanvasCoord(data.balls[ball].position);
                    $scope.gameState.balls[ball].radius = data.balls[ball].radius / 0.618033;
                }
                for (var paddle in data.paddles) {
                    $scope.gameState.players[paddle].position = transformToCanvasCoord(data.paddles[paddle].position);
                    data.paddles[paddle].dimensions = transformToCanvasCoord(data.paddles[paddle].dimensions);
                    $scope.gameState.players[paddle].width = data.paddles[paddle].dimensions[0];
                    $scope.gameState.players[paddle].height = data.paddles[paddle].dimensions[1];
                    $scope.gameState.players[paddle].score = data.paddles[paddle].score;
                }
            }

            function initState (data) {
                for (var ball in data.balls) {
                    $scope.gameState.balls[ball] = {};
                    $scope.gameState.balls[ball].position = transformToCanvasCoord(data.balls[ball].position);
                    $scope.gameState.balls[ball].radius = data.balls[ball].radius / 0.618033;
                    $scope.gameState.balls[ball].velocity = [0.0,0.0];
                    $scope.gameState.balls[ball].color = [Math.random(), Math.random(), Math.random(), 1.0];
                }
                for (var paddle in data.paddles) {
                    $scope.gameState.players[paddle] = {};
                    $scope.gameState.players[paddle].position = transformToCanvasCoord(data.paddles[paddle].position);
                    $scope.gameState.players[paddle].velocity = [0.0,0.0];
                    $scope.gameState.players[paddle].refVelocity = [0.0,0.0];
                    $scope.gameState.players[paddle].acceleration = [0.0,2.0];
                    data.paddles[paddle].dimensions = transformToCanvasCoord(data.paddles[paddle].dimensions);
                    $scope.gameState.players[paddle].width = data.paddles[paddle].dimensions[0];
                    $scope.gameState.players[paddle].height = data.paddles[paddle].dimensions[1];
                    $scope.gameState.players[paddle].color = [Math.random(), Math.random(), Math.random(), 1.0];
                    $scope.gameState.players[paddle].score = data.paddles[paddle].score;
                    $scope.updateStyle();
                }
                console.log($scope.gameState)
            }

            function updatePaddleSpeed(paddle) {
                BattlePongService.setPaddleSpeed(paddle.velocity[1], function() {
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
                BattlePongService.getState($scope.currentPlayer.currentGame.id, function (data) {
                    setState(data);
                    if ($scope.gameOn == true) {
                        updateState();
                    }
                });
            }

            function startStuff() {
                playerService.getPlayer(function (data) {
                    $scope.currentPlayer = data.player;
                    BattlePongService.getState($scope.currentPlayer.currentGame.id, function (data) {
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
                    BattlePongService.handleWallBounce(ball);
		            for (paddle in $scope.gameState.paddles){
			            BattlePongService.handlePaddleBounce(ball, $scope.gameState.paddles[paddle])
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
