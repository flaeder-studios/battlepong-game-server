(function () {

    angular.module('flaederGamesApp')
        .factory('BattlePongService', [function () {

            var service = {};

            service.BALL_EDGES = 32;
            service.D_ANGLE = 2 * Math.PI / service.BALL_EDGES;
            service.canvas = angular.element("#gameCanvas")[0];
            service.screenRatio = service.canvas.height / service.canvas.width;
            service.gl = setupWebGL(service.canvas);

            service.initGame = function (vertexShader, fragmentShader) {
                this.gl.viewportWidth = this.canvas.width;
                this.gl.viewportHeight = this.canvas.height;

                this.program = createProgramFromScripts(this.gl, [vertexShader, fragmentShader]);

                // setup GLSL program
                this.gl.useProgram(this.program);

                // look up where the vertex data needs to go.
                this.positionLocation = this.gl.getAttribLocation(this.program, "aVertexPosition");
                this.colorLocation = this.gl.getUniformLocation(this.program, "uColor");
                this.translationLocation = this.gl.getUniformLocation(this.program, "uTranslation");
                this.scaleLocation = this.gl.getUniformLocation(this.program, "uScale");
            };

            service.ballBuffer = [0.0, 0.0];

            var angle = 0.0,
                i;
            for (i = 2; i < 2 * (service.BALL_EDGES + 1) + 2; i += 2) {
                service.ballBuffer[i] = Math.cos(angle) * service.screenRatio;
                service.ballBuffer[i + 1] = Math.sin(angle);
                angle += service.D_ANGLE;
            }

            service.paddleBuffer = [
                service.screenRatio, 1.0,
                -service.screenRatio, 1.0,
                -service.screenRatio, -1.0,
                service.screenRatio, -1.0
            ];

            service.drawBall = function (ball) {
                var buffer = this.gl.createBuffer();
                this.gl.bindBuffer(this.gl.ARRAY_BUFFER, buffer);
                this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.ballBuffer), this.gl.STATIC_DRAW);
                this.gl.enableVertexAttribArray(this.gl.positionLocation);
                this.gl.vertexAttribPointer(this.positionLocation, 2, this.gl.FLOAT, false, 0, 0);

                this.gl.uniform4fv(this.colorLocation, ball.color);
                this.gl.uniform2fv(this.translationLocation, ball.position);
                this.gl.uniform2fv(this.scaleLocation, [ball.radius, ball.radius]);

                // draw
                this.gl.drawArrays(this.gl.TRIANGLE_FAN, 0, this.ballBuffer.length / 2);
            };

            service.handleWallBounce = function (ball) {
                // check wall bounce
                if (ball.position[0] + ball.radius > 1) {
                    ball.velocity[0] = -ball.velocity[0];
                    ball.position[0] = 0.9999 - ball.radius;
                } else if (ball.position[0] - ball.radius < -1) {
                    ball.velocity[0] = -ball.velocity[0];
                    ball.position[0] = -0.9999 + ball.radius;
                } else if (ball.position[1] + ball.radius > 1) {
                    ball.velocity[1] = -ball.velocity[1];
                    ball.position[1] = 0.9999 - ball.radius;
                } else if (ball.position[1] - ball.radius < -1) {
                    ball.velocity[1] = -ball.velocity[1];
                    ball.position[1] = -0.9999 + ball.radius;
                }
            };

            service.handlePaddleBounce = function (ball, paddle) {
                if (Math.abs(ball.position[0] - paddle.position[0]) < ball.radius + paddle.width / 2 &&
                    Math.abs(ball.position[1] - paddle.position[1]) < paddle.height) {
                    // collision!!
                    if (ball.velocity[0] < 0) {
                        ball.position[0] = paddle.position[0] + paddle.width / 2 + ball.radius + 0.00001;
                    } else {
                        ball.position[0] = paddle.position[0] - paddle.width / 2 - ball.radius - 0.00001;
                    }
                    ball.velocity[0] = -ball.velocity[0];
                } else if (Math.abs(ball.position[1] - paddle.position[1]) < ball.radius + paddle.height / 2 &&
                    Math.abs(ball.position[0] - paddle.position[0]) < paddle.width) {
                    // collision!!
                    if (ball.velocity[1] < 0) {
                        ball.position[1] = paddle.position[1] + paddle.height / 2 + ball.radius + 0.00001;
                    } else {
                        ball.position[1] = paddle.position[1] - paddle.height / 2 - ball.radius - 0.00001;
                    }
                    ball.velocity[1] = -ball.velocity[1];
                }
            };

            service.moveBall = function (ball, dt) {
                ball.position[0] += ball.velocity[0] * dt;
                ball.position[1] += ball.velocity[1] * dt;

                if (ball.position[0] > 1.0) {
                    ball.position[0] = 1.0;
                }

                if (ball.position[0] < -1.0) {
                    ball.position[0] = -1.0;
                }

                if (ball.position[1] > 1.0) {
                    ball.position[1] = 1.0;
                }

                if (ball.position[1] < -1.0) {
                    ball.position[1] = -1.0;
                }

            };

            service.movePaddle = function (paddle, dt) {
                // calculate speed
                paddle.velocity[0] += (paddle.refVelocity[0] - paddle.velocity[0]) * paddle.acceleration[0] * dt;
                paddle.velocity[1] += (paddle.refVelocity[1] - paddle.velocity[1]) * paddle.acceleration[1] * dt;

                // Update position
                paddle.position[0] += paddle.velocity[0] * dt;
                paddle.position[1] += paddle.velocity[1] * dt;

                // limit position
                if (paddle.position[0] + paddle.width / 2 > 1.0) {
                    paddle.position[0] = 1.0 - paddle.width / 2;
                    paddle.velocity[0] = 0.0;
                }
                if (paddle.position[0] - paddle.width / 2 < -1.0) {
                    paddle.position[0] = -1.0 + paddle.width / 2;
                    paddle.velocity[0] = 0.0;
                }
                if (paddle.position[1] + paddle.height / 2 > 1.0) {
                    paddle.position[1] = 1.0 - paddle.height / 2;
                    paddle.velocity[1] = 0.0;
                }
                if (paddle.position[1] - paddle.height / 2 < -1.0) {
                    paddle.position[1] = -1.0 + paddle.height / 2;
                    paddle.velocity[1] = 0.0;
                }
            };

            service.drawPaddle = function (paddle) {
                var buffer = this.gl.createBuffer();
                this.gl.bindBuffer(this.gl.ARRAY_BUFFER, buffer);
                this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.paddleBuffer), this.gl.STATIC_DRAW);
                this.gl.enableVertexAttribArray(this.gl.positionLocation);
                this.gl.vertexAttribPointer(this.gl.positionLocation, 2, this.gl.FLOAT, false, 0, 0);
                this.gl.uniform4fv(this.colorLocation, paddle.color);

                this.gl.uniform4fv(this.colorLocation, paddle.color);
                this.gl.uniform2fv(this.translationLocation, paddle.position);
                this.gl.uniform2fv(this.scaleLocation, [paddle.width / 2, paddle.height / 2]);

                // draw
                this.gl.drawArrays(this.gl.TRIANGLE_FAN, 0, this.paddleBuffer.length / 2);
            };

            return service;

        }]);

})();
