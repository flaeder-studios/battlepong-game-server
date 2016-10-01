import numpy as np


class Paddle:
    def __init__(self, position=None, dimensions=None):
        if position is None and dimensions is None:
            self.dimensions = np.array((0., 0.))
            self.position = np.array((0., 0.))
        elif dimensions is None:
            self.position = np.array(position)
            self.dimensions = np.array((0., 0.))
        else:
            self.position = np.array(position)
            self.dimensions = np.array(dimensions)
        self.halfDim = self.dimensions / 2.
        self.points = 0
        self.velocity = np.array((0., 0.))

    def __str__(self):
        return 'Position: {}\nDimensions: {}\nPoints: {}'.format(self.position, self.dimensions, self.points)


class Ball:
    def __init__(self, position=None, radius=None, speed=None):
        if position is None and radius is None and speed is None:
            self.position = np.array((0., 0.))
            self.radius = 0.
            self.speed = 0.

        elif position is None and radius is None:
            self.position = np.array((0., 0.))
            self.radius = 0.
            self.speed = speed
        elif position is None:
            self.position = np.array((0., 0.))
            self.radius = radius
            self.speed = speed
        else:
            self.position = np.array(position)
            self.radius = radius
            self.speed = speed
        self.velocity = np.array((1, 0)) * self.speed

    def __str__(self):
        return 'Position: {}\nRadius: {}\nSpeed: {}\nVelocity: {}'.format(self.position, self.radius, self.speed, self.velocity)


class Game:
    """This is a game of PONG. A game is initialized with  the paddles and ball that it will use. This will set
    the paddles and ball in relation to the gameboard. The gameboard can check that things dont
    collide. If the ball go past a paddle the other paddle get one point."""
    def __init__(self, center, dimensions, leftPaddle, rightPaddle, ball, ballSpeed=None):
        """Initialize a gameboard with paddles and ball. Paddles and ball will get
        positions in relation to the gameboard. The center of gameboard is its position
        and the dimensions of gameboard is dimensions."""
        self.center = np.array(center)
        self.dimensions = np.array((dimensions))
        self.halfDim = self.dimensions / 2.
        self.paddles = [leftPaddle, rightPaddle]
        self.ball = ball
        leftPaddle.dimensions = np.array((self.dimensions[1] / (16. * 3), self.dimensions[1] / 16.))
        rightPaddle.dimensions = np.array((self.dimensions[1] / (16. * 3), self.dimensions[1] / 16.))
        leftPaddle.position = np.array((center[0] - self.halfDim[0], center[1]))
        rightPaddle.position = np.array((center[0] + self.halfDim[0], center[1]))
        ball.position = np.array(center)
        ball.radius = leftPaddle.dimensions[1] / 32.
        if ballSpeed is not None:
            ball.speed = ballSpeed
        else:
            ball.speed = self.dimensions[0] / 6.

    def collision(self):
        """Check for collisions on the gameboard. If ball collide change velocity of ball.
        Give points to paddles as necessary."""
        self.paddleWallCollision()
        self.paddleBallCollision()
        self.ballWallCollision()
    
    def paddleWallCollision(self):
        """Help method to method collision."""
        Topp = self.center + self.halfDim
        Bott = self.center - self.halfDim
        for paddle in self.paddles:
            if paddle.position[1] > Topp[1] - paddle.halfDim[1]:
                paddle.position[1] = Topp[1] - paddle.halfDim[1]
            elif paddle.position[1] < Bott[1] + paddle.halfDim[1]:
                paddle.position[1] = Bott[1] + paddle.halfDim[1]

    def paddleBallCollision(self):
        """Help method to method collision."""
        ball = self.ball
        leftPaddle = self.paddles[0]
        rightPaddle = self.paddles[1]
        convertToRadians = (np.pi / 4.) / leftPaddle.halfDim[1]
        if ball.position[0] < leftPaddle.position[0] + leftPaddle.halfDim[0] + ball.radius:
            if self.isPaddleBallColliding(ball, leftPaddle):
                ball.position[0] = leftPaddle.position[0] + leftPaddle.halfDim[0] + ball.radius
                radians = convertToRadians * (ball.position[1] - leftPaddle.position[1])
                ball.velocity = np.array((np.cos(radians), np.sin(radians))) * ball.speed
            else:
                rightPaddle.points = rightPaddle.points + 1
                ball.position = np.array(self.center)
                ball.velocity = np.array((ball.speed, 0))
        elif ball.position[0] > rightPaddle.position[0] - rightPaddle.halfDim[0] - ball.radius:
            if self.isPaddleBallColliding(ball, rightPaddle):
                ball.position[0] = rightPaddle.position[0] - rightPaddle.halfDim[0] - ball.radius
                radians = convertToRadians * (rightPaddle.position[1] - ball.position[1])
                ball.velocity = np.array((np.cos(np.pi + radians), np.sin(np.pi + radians))) * ball.speed
            else:
                leftPaddle.points = leftPaddle.points + 1
                ball.position = np.array(self.center)
                ball.velocity = np.array((-ball.speed, 0))

    def isPaddleBallColliding(self, ball, paddle):
        """Help method to method paddleBallCollision."""
        if ball.position[1] > paddle.position[1] + paddle.halfDim[1]:
            return False
        elif ball.position[1] < paddle.position[1] - paddle.halfDim[1]:
            return False
        else:
            return True

    def ballWallCollision(self):
        """Help method to method collision."""
        ball = self.ball
        if ball.position[1] > self.center[1] + self.halfDim[1] - ball.radius:
            ball.position[1] = self.center[1] + self.halfDim[1] - ball.radius
            ball.velocity[1]= -ball.velocity[1]
        elif ball.position[1] < self.center[1] - self.halfDim[1] + ball.radius:
            ball.position[1] = self.center[1] - self.halfDim[1] + ball.radius
            ball.velocity[1] = -ball.velocity[1]

    def __str__(self):
        return 'Position: {}\nDimensions: {}'.format(self.center, self.dimensions)
