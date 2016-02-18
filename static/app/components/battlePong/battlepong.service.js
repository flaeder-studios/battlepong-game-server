(function () {

    angular.module('flaederGamesApp')
        .factory('BattlePongService', [function () {

            var service = {};

            service.BALL_EDGES = 32;
            service.D_ANGLE = 2 * Math.PI / service.BALL_EDGES;
            service.canvas = angular.element("#battlePongCanvas")[0];
            service.screenRatio = service.canvas.height / service.canvas.width;

            service.initGame = function (vertexShader, fragmentShader) {
                this.gl = this.canvas.getContext('experimental-webgl');
                if (!this.gl) {
                    console.error("could not get webGL context...");
                    return;
                }

                this.gl.viewportWidth = this.canvas.width;
                this.gl.viewportHeight = this.canvas.height;

                this.program = createProgramFromScripts(this.gl, [vertexShader, fragmentShader]);

                // setup GLSL program
                this.gl.useProgram(this.program);

                // look up where the vertex data needs to go.
                this.positionLocation = this.gl.getAttribLocation(this.program, "aVertexPosition");
            };

            service.drawBoard = function (board) {

            };

            service.ballBuffer = [0.0, 0.0];

            var angle = 0.0,
                i;
            for (i = 2; i < 2 * (service.BALL_EDGES + 1) + 2; i += 2) {
                service.ballBuffer[i] = Math.cos(angle) * service.screenRatio;
                service.ballBuffer[i + 1] = Math.sin(angle);
                angle += service.D_ANGLE;
            }


            service.drawBall = function (ball) {
                var buffer = this.gl.createBuffer();
                this.gl.bindBuffer(this.gl.ARRAY_BUFFER, buffer);
                this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.ballBuffer), this.gl.STATIC_DRAW);
                this.gl.enableVertexAttribArray(this.gl.positionLocation);
                this.gl.vertexAttribPointer(this.gl.positionLocation, 2, this.gl.FLOAT, false, 0, 0);

                // draw
                this.gl.drawArrays(this.gl.TRIANGLE_FAN, 0, this.ballBuffer.length / 2);
            };

            service.drawPaddle = function (paddle) {

            };

            service.createBoard = function () {
                return {
                    balls: [],
                    paddles: [],

                    aspectRatio: 0.75,
                    boardEdge: 0.05,

                    createBall: function (radius) {
                        var b = {};

                        b.xspd = 0.0;
                        b.yspd = 0.0;
                        b.xpos = 0.0;
                        b.ypos = 0.0;
                        b.radius = radius;

                        b.draw = function (gl) {

                        };

                        b.move = function (x, y) {
                            this.xpos = x;
                            this.ypos = y;
                        };

                        b.moveBy = function (dt) {
                            this.xpos += dt * this.xspd;
                            this.ypos += dt * this.yspd;
                        };

                        b.setVelocity = function (dx, dy) {
                            this.xspd = dx;
                            this.yspd = dy;
                        };

                        b.getXPos = function () {
                            return this.xpos;
                        };

                        b.getYPos = function () {
                            return this.ypos;
                        };

                        b.handleCollision = function () {
                            if (this.xpos + this.radius > 1) {
                                this.xspd = -this.xspd;
                                this.xpos = 0.9999 - this.radius;
                            } else if (this.xpos - this.radius < -1) {
                                this.xspd = -this.xspd;
                                this.xpos = -0.9999 + this.radius;
                            } else if (this.ypos + this.radius > 1) {
                                this.yspd = -this.yspd;
                                this.ypos = 0.9999 - this.radius;
                            } else if (this.ypos - this.radius < -1) {
                                this.yspd = -this.yspd;
                                this.ypos = -0.9999 + this.radius;
                            }
                        };

                        this.balls.push(b);
                    },

                    createPaddle: function (width) {
                        var p = {};

                        p.width = width;
                        p.length = 0.2;
                        p.xpos = 0.0;
                        p.ypos = 0.0;
                        p.velocity = 0.0;

                        p.draw = function (gl) {
                            // Create a buffer and put a single clipspace rectangle in
                            // it (2 triangles)
                            var buffer = gl.createBuffer();
                            gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
                            gl.bufferData(
                                gl.ARRAY_BUFFER,
                                new Float32Array([
                            this.xpos, this.ypos,
                            this.xpos, this.ypos + this.length,
                            this.xpos - this.width, this.ypos + this.length,
                            this.xpos, this.ypos,
                            this.xpos - this.width, this.ypos,
                            this.xpos - this.width, this.ypos + this.length]),
                                gl.STATIC_DRAW
                            );
                            gl.enableVertexAttribArray(gl.positionLocation);
                            gl.vertexAttribPointer(gl.positionLocation, 2, gl.FLOAT, false, 0, 0);

                            // draw
                            gl.drawArrays(gl.TRIANGLES, 0, 6);
                        };

                        p.move = function (x, y) {
                            this.xpos = x;
                            this.ypos = y;
                        };

                        p.moveBy = function (dt) {
                            this.ypos += dt * this.velocity;
                        };

                        p.setVelocity = function (dy) {
                            this.velocity = dy;
                        };

                        p.getPos = function () {
                            return this.ypos;
                        };

                        p.handleCollision = function () {
                            if (this.ypos < -0.9999) {
                                this.ypos = -0.9999;
                                this.velocity = -this.velocity;
                            } else if (this.ypos > 0.9999) {
                                this.ypos = 0.9999;
                                this.velocity = -this.velocity;
                            }
                        };

                        this.paddles.push(p);

                    },

                    draw: function (gl) {
                        var i;

                        for (i = 0; i < this.paddles.length; i++) {
                            this.paddles[i].draw(gl);
                        }

                        for (i = 0; i < this.balls.length; i++) {
                            this.balls[i].draw(gl);
                        }

                    },

                    updatePositions: function (dt) {
                        var i;

                        for (i = 0; i < this.paddles.length; i++) {
                            this.paddles[i].moveBy(dt);
                            this.paddles[i].handleCollision();
                        }

                        for (i = 0; i < this.balls.length; i++) {
                            this.balls[i].moveBy(dt);
                            this.balls[i].handleCollision();
                        }

                    },

                    update: function (dt, gl) {
                        this.updatePositions(dt);
                        this.draw(gl);
                    }
                };
            }

            return service;

        }]);

})();
