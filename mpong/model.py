import random
import math
from random import randrange

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

    def dot(self, vec):
        return self.x * vec.x + self.y * vec.y


class Rectangle(object):
    def __init__(self, pos_x, pos_y, width, height):
        self.position = Vector(pos_x, pos_y)
        self.width = Vector(width, 0)
        self.height = Vector(0, height)
        self.speed = Vector(0, 0)

    def topp(self):
        return self.position.y + self.height.y / 2.

    def bottom(self):
        return self.position.y - self.height.y / 2.

    def left(self):
        return self.position.x - self.width.x / 2.

    def right(self):
        return self.position.x + self.width.x / 2.

    def move(self):
        self.position.x += self.speed.x
        self.position.y += self.speed.y


class Player(Rectangle):
    def __init__(self, name, pos_x, pos_y, width, height):
        super(Player, self).__init__(pos_x, pos_y, width, height)
        self.name = name
        self.points = 0


class Ball(Rectangle):
    def __init__(self, pos_x, pos_y, width):
        super(Ball, self).__init__(pos_x, pos_y, width, width)
        self.speed = Vector(1, 1)
        self.init_speed = 0

    def reset(self, pos):
        self.position = Vector(0, 0).add(pos)
        if random.random() < 0.5:
            alpha = -75.0 * math.pi / 180 + (2 * 75.0) * math.pi / 180 * random.random()
        else:
            alpha = (180 - 75) * math.pi / 180 + (2 * 75.0) * math.pi / 180 * random.random()
        x = abs(self.init_speed) * math.cos(alpha)
        y = abs(self.init_speed) * math.sin(alpha)
        self.speed = Vector(x, y)


class Gameboard(Rectangle):
    def __init__(self, player1_name, player2_name, width, height):
        print "Gameboard: width(%f), height(%f)" % (width, height)
        super(Gameboard, self).__init__(width / 2., -height / 2.,
                                        width, height)
        self.player_scale_factor = 12
        self.player_height = width / self.player_scale_factor
        self.player_width = height / self.player_scale_factor
        self.player1 = Player(player1_name,
                              self.position.x - width / 2. + self.player_width / 2.,
                              self.position.y,
                              self.player_width, self.player_height)
        self.player2 = Player(player2_name,
                              self.position.x + width / 2. - self.player_width / 2.,
                              self.position.y,
                              self.player_width, self.player_height)
        self.ball = Ball(self.position.x, self.position.y, height / 30.)


class Game(object):
    def __init__(self, height, name1, name2, ball_initial_speed):
        self.golden_ratio = 1.618033
        self.width = self.golden_ratio * float(height)
        self.game = Gameboard(name1, name2, self.width, height)
        self.game.ball.init_speed = ball_initial_speed
        self.game.ball.reset(self.game.position)

    def collision(self):
        # check if players or ball hit roof or bottom
        for obj in [self.game.player1, self.game.player2]:
            if obj.topp() > self.game.topp():
                obj.position.y = self.game.topp() - obj.height.y / 2.
                obj.speed.y = 0
            elif obj.bottom() < self.game.bottom():
                obj.position.y = self.game.bottom() + obj.height.y / 2.
                obj.speed.y = 0
        if self.game.ball.topp() > self.game.topp():
            self.game.ball.position.y = self.game.topp() - self.game.ball.height.y / 2.
            self.game.ball.speed.y = -self.game.ball.speed.y
        elif self.game.ball.bottom() < self.game.bottom():
            self.game.ball.position.y = self.game.bottom() + self.game.ball.height.y / 2.
            self.game.ball.speed.y = -self.game.ball.speed.y

        # check if ball bounces off a player and if a player get points
        # the ball bounces off in a direction calculated from where it hits the paddle.
        ball = self.game.ball
        player2 = self.game.player2
        player1 = self.game.player1
        game = self.game
        radians_top = math.atan(game.height.y / game.width.x) * 2.365 # approx 75 degrees
        height_to_radians = radians_top / (player1.height.y / 2.0) 
        if ball.speed.dot(Vector(1, 0)) > 0:
            if ball.right() > player2.left():
                if ball.position.y < player2.topp() and ball.position.y > player2.bottom():
                    ball.position.x = player2.left() - ball.width.x / 2.
                    diff_y = ball.position.y - player2.position.y
                    radians = diff_y * height_to_radians
                    ball.speed.x = ball.init_speed * math.cos(math.pi - radians)
                    ball.speed.y = ball.init_speed * math.sin(math.pi - radians)
                else:
                    player1.points += 1
                    ball.reset(self.game.position)
        else:
            if ball.left() < player1.right():
                if ball.position.y < player1.topp() and ball.position.y > player1.bottom():
                    ball.position.x = player1.right() + ball.width.x / 2.
                    diff_y = ball.position.y - float(player1.position.y)
                    radians = diff_y * height_to_radians
                    ball.speed.x = ball.init_speed * math.cos(radians)
                    ball.speed.y = ball.init_speed * math.sin(radians)
                else:
                    player2.points += 1
                    ball.reset(self.game.position)

    def update(self):
        """ Move objects to new positions determined by speed"""
        self.game.ball.move()
        self.game.player1.move()
        self.game.player2.move()
        self.collision()

    def artificial_intelligence(self):
        eps = self.game.player2.height.y / 8. # player2 target area
        if self.game.ball.speed.dot(Vector(1., 0.)) > 0:
            self.artificial_move(self.game.player2, self.game.ball, eps)
        else:
            self.artificial_move(self.game.player2, self.game, eps)

    def artificial_move(self, paddle, obj, eps):
            if paddle.position.y < obj.position.y - eps:
                paddle.speed.y = abs(paddle.speed.y)
            elif paddle.position.y > obj.position.y + eps:
                paddle.speed.y = -abs(paddle.speed.y)
            else:
                paddle.speed.y = 0

    def clear(self):
        self.game.player1.position.y = self.game.position.y
        self.game.player2.position.y = self.game.position.y
        self.game.ball.position.x = self.game.position.x
        self.game.ball.position.y = self.game.position.y
        self.game.player1.points = 0
        self.game.player2.points = 0

    def __str__(self):
        player1_pos_y = self.game.player1.position.y
        player2_pos_y = self.game.player2.position.y
        ball_pos_x = self.game.ball.position.x
        ball_pos_y = self.game.ball.position.y
        s = ""
        s += "self.game.player1.position.y = %f\n" % (player1_pos_y)
        s += "self.game.player2.position.y = %f\n" % (player2_pos_y)
        s += "self.game.ball.position. = (%f,%f)\n" % (ball_pos_x, ball_pos_y)
        s += "player1.points = %d\n" % (self.game.player1.points)
        s += "player2.points = %d\n" % (self.game.player2.points)
        return s


if __name__ == "__main__":
    g = Game(100, "Clint", "Rudolf")
    while True:
        g.update()
        g.artificial_intelligence()
        print g
