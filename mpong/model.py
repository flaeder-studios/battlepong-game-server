
class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

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
        self.speed.x = 1
        self.speed.y = 1


class Gameboard(Rectangle):
    def __init__(self, player1_name, player2_name, width, height):
        super(Gameboard, self).__init__(width / 2., -height / 2.,
                                        width, height)
        self.player1 = Player(player1_name,
                              self.position.x - self.width.x / 2.,
                              self.position.y,
                              height / 6, width / 6.)
        self.player2 = Player(player2_name,
                              self.position.x + self.width.x / 2.,
                              self.position.y,
                              height / 6, width / 6.)
        self.ball = Ball(self.position.x, self.position.y, height / 30.)


class Game(object):
    def __init__(self, height, name1, name2):
        self.golden_ratio = 1.618033
        self.width = self.golden_ratio * float(height)
        self.game = Gameboard(name1, name2, self.width, height)

    def collision(self):
        # check if players or ball hit roof or floor
        for obj in [self.game.player1, self.game.player2]:
            if obj.topp() > self.game.topp():
                obj.position.y = self.game.topp() - obj.height.y / 2.
                obj.speed.y = -obj.speed.y
            elif obj.bottom() < self.game.bottom():
                obj.position.y = self.game.bottom() + obj.height.y / 2.
                obj.speed.y = -obj.speed.y

        # check if ball bounces off a player, or if a player get points
        ball = self.game.ball
        player2 = self.game.player2
        player1 = self.game.player1
        game = self.game
        if ball.speed.dot(Vector(1, 0)) > 0:
            if ball.right() > player2.left():
                if ball.position.y < player2.topp() and ball.position.y > player2.bottom():
                    ball.speed.x = -ball.speed.x
                else:
                    player1.points += 1
                    ball.position.x = game.position.x
                    ball.position.y = game.position.y
        else:
            if ball.left() < player1.right():
                if ball.position.y < player1.topp() and ball.position.y > player1.bottom():
                    ball.speed.x = -ball.speed.x
                else:
                    player2.points += 1
                    ball.position.x = game.position.x
                    ball.position.y = game.position.y

    def update(self, player1_speed_y):
        ball = self.game.ball
        player1 = self.game.player1
        player2 = self.game.player2
        player1.speed.y = player1_speed_y
        ball.move()
        self.game.player1.move()
        # artificial intelligence move player2
        if ball.speed.dot(Vector(1., 0.)) > 0:
            if player2.position.y < ball.position.y:
                player2.speed.y = 1
            elif player2.y > ball.position.y:
                player2.speed.y = -1
        else:
            eps = 0.000001
            if player2.position.y < self.game.position.y - eps:
                player2.speed.y = 1
            elif player2.position.y > self.game.position.y + eps:
                player2.speed.y = -1
            else:
                player2.speed.y = 0
        player2.move()
        self.collision()
        player1_pos_y = self.game.player1.position.y
        player2_pos_y = self.game.player2.position.y
        ball_pos_x = self.game.ball.position.x
        ball_pos_y = self.game.ball.position.y
        print "self.game.player1.position.y = %f" % (player1_pos_y)
        print "self.game.player2.position.y = %f" % (player2_pos_y)
        print "self.game.ball.position. = (%f,%f)" % (ball_pos_x, ball_pos_y)
        print "player1.points = %d" % (self.game.player1.points)
        print "player2.points = %d" % (self.game.player2.points)

    def clear(self):
        self.game.player1.position.y = self.game.position.y
        self.game.player2.position.y = self.game.position.y
        self.game.ball.position.x = self.game.position.x
        self.game.ball.position.y = self.game.position.y
        self.game.player1.points = 0
        self.game.player2.points = 0


if __name__ == "__main__":
    g = Game(100, "Clint", "Rudolf")
