import threading
import time
import random
import math
from random import random


class Vector(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def add(self, vec):
        temp = Vector(self.x, self.y)
        temp.x += vec.x
        temp.y += vec.y
        return temp

    def subtract(self, vec):
        temp = Vector(self.x, self.y)
        temp.x -= vec.x
        temp.y -= vec.y
        return temp

    def multiply(self, n):
        temp = Vector(self.x, self.y)
        temp.x *= temp.x * n
        temp.y *= temp.y * n
        return temp

    def copy(self):
        temp = Vector(self.x, self.y)
        return temp

    def dot(self, vec):
        return self.x * vec.x + self.y * vec.y


class Rectangle(object):
    def __init__(self, name, posX, posY, width, height):
        self.position = Vector(posX, posY)
        self.width = Vector(width, 0)
        self.height = Vector(0, height)
        self.velocity = Vector(0, 0)
        self.name = name

    def topp(self):
        return self.position.y + self.height.y / 2.

    def bottom(self):
        return self.position.y - self.height.y / 2.

    def left(self):
        return self.position.x - self.width.x / 2.

    def right(self):
        return self.position.x + self.width.x / 2.

    def move(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y


class Paddle(Rectangle):
    def __init__(self, name, posX, posY, width, height):
        super(Paddle, self).__init__(name, posX, posY, width, height)
        self.points = 0


class Ball(Rectangle):
    def __init__(self, name, posX, posY, width):
        super(Ball, self).__init__(posX, posY, width, width)
        self.velocity = Vector(1, 1)
        self.initSpeed = 0

    def reset(self, pos):
        self.position = Vector(0, 0).add(pos)
        if random.random() < 0.5:
            alpha = -75.0 * math.pi / 180 + (2 * 75.0) * math.pi / 180 * random.random()
        else:
            alpha = (180 - 75) * math.pi / 180 + (2 * 75.0) * math.pi / 180 * random.random()
        x = abs(self.initSpeed) * math.cos(alpha)
        y = abs(self.initSpeed) * math.sin(alpha)
        self.velocity = Vector(x, y)


class Gameboard(Rectangle):
    def __init__(self, paddle1Name, paddle2Name, width, height):
        super(Gameboard, self).__init__('pong', width / 2., -height / 2.,
                                        width, height)
        self.paddleScaleFactor = 12
        self.paddleHeight = width / self.paddleScaleFactor
        self.paddleWidth = height / self.paddleScaleFactor
        self.paddle1 = Paddle(paddle1Name,
                              self.position.x - width / 2. + self.paddleWidth / 2.,
                              self.position.y,
                              self.paddleWidth, self.paddleHeight)
        self.paddle2 = Paddle(paddle2Name,
                              self.position.x + width / 2. - self.paddleWidth / 2.,
                              self.position.y,
                              self.paddleWidth, self.paddleHeight)
        self.ball = Ball('gameBall', self.position.x, self.position.y, height / 30.)


class Game(object):
    def __init__(self, height, name1, name2, ballInitialSpeed):
        self.goldenRatio = 1.618033
        self.width = self.goldenRatio * float(height)
        self.game = Gameboard(name1, name2, self.width, height)
        self.game.ball.initSpeed = ballInitialSpeed
        self.game.ball.reset(self.game.position)

    def collision(self):
        # check if paddles or ball hit roof or bottom
        for obj in [self.game.paddle1, self.game.paddle2]:
            if obj.topp() > self.game.topp():
                obj.position.y = self.game.topp() - obj.height.y / 2.
                obj.velocity.y = 0
            elif obj.bottom() < self.game.bottom():
                obj.position.y = self.game.bottom() + obj.height.y / 2.
                obj.velocity.y = 0
        if self.game.ball.topp() > self.game.topp():
            self.game.ball.position.y = self.game.topp() - self.game.ball.height.y / 2.
            self.game.ball.velocity.y = -self.game.ball.velocity.y
        elif self.game.ball.bottom() < self.game.bottom():
            self.game.ball.position.y = self.game.bottom() + self.game.ball.height.y / 2.
            self.game.ball.velocity.y = -self.game.ball.velocity.y

        # check if ball bounces off a paddle and if a paddle get points
        # the ball bounces off in a direction calculated from where it hits the paddle.
        ball = self.game.ball
        paddle2 = self.game.paddle2
        paddle1 = self.game.paddle1
        game = self.game
        radiansTop = math.atan(game.height.y / game.width.x) * 2.365 # approx 75 degrees
        heightToRadians = radiansTop / (paddle1.height.y / 2.0) 
        if ball.velocity.dot(Vector(1, 0)) > 0:
            if ball.right() > paddle2.left():
                if ball.position.y < paddle2.topp() and ball.position.y > paddle2.bottom():
                    ball.position.x = paddle2.left() - ball.width.x / 2.
                    diffY = ball.position.y - paddle2.position.y
                    radians = diffY * heightToRadians
                    ball.velocity.x = ball.initSpeed * math.cos(math.pi - radians)
                    ball.velocity.y = ball.initSpeed * math.sin(math.pi - radians)
                else:
                    paddle1.points += 1
                    ball.reset(self.game.position)
        else:
            if ball.left() < paddle1.right():
                if ball.position.y < paddle1.topp() and ball.position.y > paddle1.bottom():
                    ball.position.x = paddle1.right() + ball.width.x / 2.
                    diffY = ball.position.y - float(paddle1.position.y)
                    radians = diffY * heightToRadians
                    ball.velocity.x = ball.initSpeed * math.cos(radians)
                    ball.velocity.y = ball.initSpeed * math.sin(radians)
                else:
                    paddle2.points += 1
                    ball.reset(self.game.position)


    def getPaddle1Speed(self):
        """returns a Vector."""
        return self.game.paddle1.velocity.copy()

    def getPaddle2Speed(self):
        """returns a Vector."""
        return self.game.paddle2.velocity.copy()

    def update(self, velocity):
        """ Move game objects (paddles and ball).
        Parameter velocity is a dictionary containing velocitys for paddle1 and paddle2.
        velocity has keys 'paddle1' and 'paddle2' with values Vector.
        """


        paddle1 = self.game.paddle1
        paddle2 = self.game.paddle2
        paddle1.velocity = velocity[paddle1.name]
        paddle2.velocity = velocity[paddle2.name]
        self.game.ball.move()
        self.game.paddle1.move()
        self.game.paddle2.move()
        self.collision()

    def getState(self):
        game = self.game
        paddle1 = game.paddle1
        paddle2 = game.paddle2
        ball = game.ball
        state = {}
        state[paddle1.name] = [paddle1.position.x, paddle1.position.y, paddle1.height, paddle1.width, paddle1.points]
        state[paddle2.name] = [paddle2.position.x, paddle2.position.y, paddle2.height, paddle2.width, paddle2.points]
        state[ball.name] = [ball.position.x, ball.position.y, ball.height, ball.width]
        state[game.name] = [game.position.x, game.position.y, game.height, game.width]
        return state

    def artificialIntelligence(self):
        eps = self.game.paddle2.height.y / 8. # paddle2 target area
        if self.game.ball.velocity.dot(Vector(1., 0.)) > 0:
            self.artificialMove(self.game.paddle2, self.game.ball, eps)
        else:
            self.artificialMove(self.game.paddle2, self.game, eps)

    def artificialMove(self, paddle, obj, eps):
            if paddle.position.y < obj.position.y - eps:
                paddle.velocity.y = abs(paddle.velocity.y)
            elif paddle.position.y > obj.position.y + eps:
                paddle.velocity.y = -abs(paddle.velocity.y)
            else:
                paddle.velocity.y = 0

    def clear(self):
        self.game.paddle1.position.y = self.game.position.y
        self.game.paddle2.position.y = self.game.position.y
        self.game.ball.position.x = self.game.position.x
        self.game.ball.position.y = self.game.position.y
        self.game.paddle1.points = 0
        self.game.paddle2.points = 0

    def __str__(self):
        paddle1PosY = self.game.paddle1.position.y
        paddle2PosY = self.game.paddle2.position.y
        ballPosX = self.game.ball.position.x
        ballPosY = self.game.ball.position.y
        s = ""
        s += "self.game.paddle1.position.y = %f\n" % (paddle1PosY)
        s += "self.game.paddle2.position.y = %f\n" % (paddle2PosY)
        s += "self.game.ball.position. = (%f,%f)\n" % (ballPosX, ballPosY)
        s += "paddle1.points = %d\n" % (self.game.paddle1.points)
        s += "paddle2.points = %d\n" % (self.game.paddle2.points)
        return s


class Player(object):
    def __init__(self, name):
        self.name = name
        self.velocity = Vector(0.0, 0.0)

    def changeName(self, name):
        if name:
            self.name = name

    def setVelocity(self, vY):
        self.velocity = Velocity(0, float(vY))

    def getVelocity(self):
        return self.velocity.copy()

class MPongGame(threading.Thread):
    def __init__(self, gameID, maxPlayers):
        super(MPongGame, self).__init__(self,target=self.run)
        self.gameID = gameID
        self.maxPlayers = maxPlayers
        self.joinedPlayers = []
        self.gameStarted = False
        self.pt = None
        self.model = None

    def joinPlayer(self, newPlayer):
        if newPlayer not in self.joinedPlayers:
            self.joinedPlayers.append(newPlayer)
            return newPlayer

    def leavePlayer(self, leavingPlayer):
        for p in self.joinedPlayers:
            if p == leavingPlayer:
                self.joinedPlayers.remove(p)
                return p

    def run(self):
        self.gameStarted = True
        self.model = Game(100, self.joinedPlayers[0].name, self.joinedPlayers[1].name, 3)
        self.pt = time.time()
        self.runModel()
        player1 = self.joinedPlayers[0]
        player2 = self.joinedPlayers[1]
        while self.gameStarted:
            t = time.time()
            dt = self.pt - t
            self.pt = t
            velocity = {}
            velocity[player1.name] = player1.getVelocity().multiply(dt)
            velocity[player2.name] = player2.getVelocity().multiply(dt)
            self.model.update(velocity)

    def stop(self):
        self.gameStarted = False

    def getState(self):
        if self.model:
            return self.model.getState()
        else:
            return None


if __name__ == "__main__":
    g = Game(100, "Clint", "Rudolf", 3)
    while True:
        g.update()
        g.artificialIntelligence()
        print g
