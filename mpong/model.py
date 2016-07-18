# -*- coding: utf-8 -*-
import math
import random
import threading
import time
import database


class Vector(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

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
        temp.x = temp.x * float(n)
        temp.y = temp.y * float(n)
        return temp

    def copy(self):
        temp = Vector(self.x, self.y)
        return temp

    def dot(self, vec):
        return self.x * vec.x + self.y * vec.y

    def unitVector(self):
        length = math.sqrt(self.dot(self))
        return self.multiply(1./length)

    def rotate(self, rad):
        temp = self.copy()
        temp.x = temp.x * math.cos(rad) + -temp.y * math.sin(rad)
        temp.y = temp.x * math.sin(rad) + temp.y * math.cos(rad)
        return temp


class Rectangle(object):
    def __init__(self, position, dimensions):
        self.position = position.copy()
        self.dimensions = dimensions.copy()

    def setPosition(self, vector):
        self.position = vector.copy()

    def getPosition(self):
        return self.position.copy()

    def getDimensions(self):
        return self.dimensions.copy()

    def getHalfDimensions(self):
        return self.dimensions.multiply(0.5)


class Paddle(Rectangle):
    def __init__(self, position, dimensions):
        super(Paddle, self).__init__(position, dimensions)
        self.points = 0

    def setPoints(self, p):
        self.points = p

    def getPoints(self):
        return self.points

    def copy(self):
        tmp = Paddle(self.getPosition(), self.getDimensions())
        return tmp


class Ball(object):
    def __init__(self, position, radius, speed):
        self.position = position.copy()
        self.radius = radius
        self.speed = speed
        self.velocity = Vector(1, 0).multiply(speed)

    def setSpeed(self, speed):
        self.speed = speed

    def getSpeed(self):
        return self.speed

    def setPosition(self, position):
        self.position = position.copy()

    def getPosition(self):
        return self.position.copy()

    def setVelocity(self, velocity):
        self.velocity = velocity.unitVector().multiply(self.speed)

    def getVelocity(self):
        return self.velocity.copy()

    def getRadius(self):
        return self.radius

    def copy(self):
        tmp = Ball(self.getPosition(), self.getRadius(), self.getSpeed())
        tmp.setVelocity(self.getVelocity())
        return tmp


class GameBoard(Rectangle):
    def __init__(self, position, dimensions):
        super(GameBoard, self).__init__( position, dimensions)

    def copy(self):
        return GameBoard(self.getPosition(), self.getDimensions())


class Game(threading.Thread):
    def __init__(self, player1, player2, leftPaddle, rightPaddle, gameBoard, ball):
        super(Game, self).__init__(target=self.run)
        self.daemon = True
        self.players = [player1, player2]
        self.paddles = [leftPaddle, rightPaddle]
        self.gameBoard = gameBoard
        self.ball = ball
        self.gameOn = False
        leftPaddle.setPosition(gameBoard.getPosition().subtract(Vector(gameBoard.getHalfDimensions().getX(), 0)))
        rightPaddle.setPosition(gameBoard.getPosition().add(Vector(gameBoard.getHalfDimensions().getX(), 0)))
        ball.setPosition(gameBoard.getPosition())
        self.n = 2 # middle position on paddle
        self.tp = 0
        self.stopGame = False

    def getGameOn(self):
        return self.gameOn

    def getLeftPlayer(self):
        return self.players[0].copy()

    def getRightPlayer(self):
        return self.players[1].copy()

    def getLeftPaddle(self):
        return self.paddles[0].copy()

    def getRightPaddle(self):
        return self.paddles[1].copy()

    def getGameBoard(self):
        return self.gameBoard.copy()

    def getBall(self):
        return self.ball.copy()

    def stop(self):
        self.stopGame = True

    def run(self):
        while not self.stopGame:
            if not self.gameOn:
                rad = random.random() * math.pi/2
                if random.random() < 0.5:
                    rad = rad - math.pi/4
                else:
                    rad = rad + math.pi * 3./4
                self.ballStart(Vector(1, 0).rotate(rad))
                time.paus(2)
                self.gameOn = True
                self.tp = time.time()
            tn = time.time()
            dt = tn  - self.tp
            self.tp = tn 
            self.moveBall(dt)
            self.collision()

    def ballStart(self, velocity):
        self.ball.setPosition(self.gameBoard.getPosition())
        self.ball.setVelocity(velocity)

    def moveBall(self, dt):
        b = self.ball
        b.setPosition(b.getPosition().add(b.getVelocity().multiply(dt)))

    def movePlayer(self, player, vector, dt):
        if self.gameOn:
            if player is self.players[0]:
                p = self.paddles[0]
                p.setPosition(p.getPosition().add(vector.multiply(dt)))
            elif player is self.players[1]:
                p = self.paddles[1]
                p.setPosition(p.getPosition().add(vector.multiply(dt)))

    def collision(self):
        if self.gameOn:
            self.paddleWallCollision()
            self.paddleBallCollision()
            self.ballWallCollision()
    
    def paddleWallCollision(self):
        g = self.gameBoard
        for pd in self.paddles:
            yTopp = g.getPosition().getY() + g.getHalfDimensions().getY()
            yBott = g.getPosition().getY() - g.getHalfDimensions().getY()
            if pd.getPosition().getY() > yTopp - pd.getHalfDimensions().getY():
                y = yTopp - pd.getHalfDimensions().getY()
                x = pd.getPosition().getX()
                vec = Vector(x, y)
                pd.setPosition(vec)
            elif pd.getPosition().getY() < yBott + pd.getHalfDimensions().getY():
                y = yBott + pd.getHalfDimensions().getY()
                x = pd.getPosition().getX()
                vec = Vector(x, y)
                pd.setPosition(vec)

    def paddleBallCollision(self):
        ball = self.ball
        x = ball.getPosition().getX()
        y = ball.getPosition().getY()
        leftPaddle = self.paddles[0]
        rightPaddle = self.paddles[1]
        xLeftRight = leftPaddle.getPosition().getX() + leftPaddle.getHalfDimensions().getX()
        xRightLeft = rightPaddle.getPosition().getX() - rightPaddle.getHalfDimensions().getX()
        if x  < xLeftRight + ball.getRadius():
            yLeftTopp = leftPaddle.getPosition().getY() + leftPaddle.getHalfDimensions().getY()
            yLeftBott = leftPaddle.getPosition().getY() - leftPaddle.getHalfDimensions().getY()
            if y > yLeftBott and y < yLeftTopp:
                x = xLeftRight + ball.getRadius()
                vec = Vector(x, y)
                xV = -ball.getVelocity().getX()
                yV = y - leftPaddle.getPosition().getY()
                vecV = Vector(xV, yV)
                ball.setPosition(vec)
                ball.setVelocity(vecV)
            else:
                rightPaddle.setPoints(rightPaddle.getPoints() + 1)
                self.gameOn = False
        elif x > xRightLeft - ball.getRadius():
            yRightTopp = rightPaddle.getPosition().getY() + rightPaddle.getHalfDimensions().getY()
            yRightBott = rightPaddle.getPosition().getY() - rightPaddle.getHalfDimensions().getY()
            if y > yRightBott and y < yRightTopp:
                x = xRightLeft - ball.getRadius()
                vec = Vector(x, y)
                xV = -ball.getVelocity().getX()
                yV = y - rightPaddle.getPosition().getY()
                vecV = Vector(xV, yV)
                ball.setPosition(vec)
                ball.setVelocity(vecV)
            else:
                leftPaddle.setPoints(leftPaddle.getPoints() + 1)
                self.gameOn = False

    def ballWallCollision(self):
        ball = self.ball
        x = ball.getPosition().getX()
        y = ball.getPosition().getY()
        xV = ball.getVelocity().getX()
        yV = ball.getVelocity().getY()
        g = self.gameBoard
        yTopp = g.getPosition().getY() + g.getHalfDimensions().getY()
        yBott = g.getPosition().getY() - g.getHalfDimensions().getY()
        if y > yTopp - ball.getRadius():
            y = yTopp - ball.getRadius()
            yV = -ball.getVelocity().getY()
        elif y < yBott + ball.getRadius():
            y = yBott + ball.getRadius()
            yV = -ball.getVelocity().getY()
        vec = Vector(x, y)
        vecV = Vector(xV, yV)
        ball.setPosition(vec)
        ball.setVelocity(vecV)

    def artificialIntelligence(self, player, vector, dt):
        """vector: positive y-directions"""
        if not self.gameOn and player not in self.players:
            return None
        paddle = None
        if player is self.players[0]:
            paddle = self.paddles[0]
        else:
            paddle = self.paddles[1]
        eps = paddle.getHalfDimensions().getY() * 2 / 5. # paddle target area
        k = random.randrange(0, 15)
        if k == 0:
            i = random.randrange(9)
            if i < 1:
                self.n = 0
            elif i < 3:
                self.n = 1
            elif i < 6:
                self.n = 2
            elif i < 8:
                self.n = 3
            else:
                self.n = 4
        ball = self.ball
        ballDirection = ball.getVelocity().dot(Vector(1., 0.))
        if paddle is self.paddles[0]:
            if ballDirection < 0.:
                self.artificialMove(paddle, ball, vector, dt, eps, self.n)
        elif paddle is self.paddles[1]:
            if ballDirection > 0.:
                self.artificialMove(paddle, ball, vector, dt, eps, self.n)

    def artificialMove(self, paddle, ball, vector, dt, eps, n):
        yBallPosition = ball.getPosition().getY()
        yPaddlePositionBott = paddle.getPosition().getY() - paddle.getHalfDimensions().getY()
        if yBallPosition < yPaddlePositionBott + n * eps:
            paddle.setPosition(paddle.getPosition().subtract(vector.multiply(dt)))
        elif yBallPosition > yPaddlePositionBott + n * eps and yBallPosition <  yPaddlePositionBott + (n + 1) * eps:
            pass
        else:
            paddle.setPosition(paddle.getPosition().add(vector.multiply(dt)))


if __name__ == '__main__':
    p1 = databaseSimple.Player('Erik')
    p2 = databaseSimple.Player('Malin')
    lPaddle = Paddle(Vector(0,0), Vector(1, 5))
    rPaddle = Paddle(Vector(0,0), Vector(1, 5))
    gameBoard = GameBoard(Vector(0,0), Vector(20, 20))
    ball = Ball(Vector(0,0), 0.2, 5)
    game = Game(p1, p2, lPaddle, rPaddle, gameBoard, ball)
