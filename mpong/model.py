
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
        self.speed = Vector(0, 0)
        self.width = Vector(width, 0)
        self.height = Vector(0, height)

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
    def __init__(self, name, pos_x, pos_y, height):
        super(Player, self).__init__(pos_x, pos_y, height, 1.6 * height)
        self.name = name
        self.points = 0


class Ball(Rectangle):
    def __init__(self, pos_x, pos_y, width):
        super(Ball, self).__init__(pos_x, pos_y, width, width)
        self.speed.x = 1
        self.speed.y = 1


class Gameboard(Rectangle):
    def __init__(self, player1_name, player2_name, height):
        super(Gameboard, self).__init__(1.6 * height / 2., -height / 2.,
                                        1.6 * height, height)
        self.player1 = Player(player1_name,
                              self.position.x - self.width.x / 2.,
                              self.position.y,
                              self.height.y / 12.)
        self.player2 = Player(player2_name,
                              self.position.x + self.width.x / 2.,
                              self.position.y,
                              self.height.y / 12.)
        self.ball = Ball(self.position.x, self.position.y, 1)

    def collision(self):
        # check that players do not get outside gameboard
        for obj in [self.player1, self.player2]:
            if obj.topp() > self.topp():
                obj.position.y = self.topp() - obj.height.y / 2.
            elif obj.bottom() < self.bottom():
                obj.position.y = self.bottom() + obj.height.y / 2.

        # check if ball bounces off roof or floor
        if self.ball.topp() > self.topp():
            self.ball.position.y = self.topp() - self.ball.height.y / 2.
            self.ball.speed.y = -self.ball.speed.y
        elif self.ball.bottom() < self.bottom():
            self.ball.position.y = self.bottom() + self.ball.height.y / 2.
            self.ball.speed.y = -self.ball.speed.y

        # check if ball bounces off a player, or if a player get points
        if self.ball.speed.dot(Vector(1, 0)) > 0:
            t = self.player2.topp() - self.ball.topp()
            b = self.player2.bottom() - self.ball.bottom()
            if self.ball.right() > self.player2.left():
                if t > 0 and b < 0:
                    self.ball.speed.x = -self.ball.speed.x
                else:
                    self.player1.points += 1
                    self.ball.position.x = self.position.x
                    self.ball.position.y = self.position.y
        else:
            t = self.player1.topp() - self.ball.topp()
            b = self.player1.bottom() - self.ball.bottom()
            if self.ball.right() > self.player2.left():
                if t > 0 and b < 0:
                    self.ball.speed.x = -self.ball.speed.x
                else:
                    self.player2.points += 1
                    self.ball.position.x = self.position.x
                    self.ball.position.y = self.position.y

    def update(self, player1_speed_y):
        self.ball.move()
        self.player1.speed.y = player1_speed_y
        self.player1.move()
        # artificial intelligence move player2
        if self.ball.speed.dot(Vector(1., 0.)) > 0:
            print "if ball.speed.dot(e_vecotr) > 0 == True"
            tmp = self.player2.position
            if tmp.y < self.ball.position.y:
                self.player2.speed.y = 1
            elif tmp.y > self.ball.position.y:
                self.player2.speed.y = -1
            self.player2.move()
        else:
            eps = 0.000001
            tmp = self.player2.position
            if tmp.y < self.position.y and self.player2.speed.y < 0:
                self.player2.speed.y = -self.player2.speed.y
            elif tmp.y > self.ball.position.y and self.player2.speed.y > 0:
                self.player2.speed.y = -self.player2.speed.y
            if tmp.y > self.position.y + eps or tmp.y < self.position.y - eps:
                self.player2.move()
        self.collision()
        print "self.player1.position.y = %f" % (self.player1.position.y)
        print "self.player2.position.y = %f" % (self.player2.position.y)
        print "self.ball.position. = (%f,%f)" % (self.ball.position.x, self.ball.position.y)
        print "player1.points = %d" % (self.player1.points)
        print "player2.points = %d" % (self.player2.points)

    def clear(self):
        self.player1.position.x = self.position.x - self.width / 2.
        self.player1.position.y = self.position.y
        self.player2.position.x = self.position.x + self.width / 2.
        self.player2.position.y = self.position.y
        self.ball.position.x = self.position.x
        self.ball.position.y = self.position.y
        self.player1.points = 0
        self.player2.points = 0


if __name__ == "__main__":
    g = Gameboard("Clint", "Rudolf", 5)
    g.update(1)
    g.update(1)
    g.update(1)
    g.update(1)
    g.update(1)
    g.update(1)
    g.update(1)
    g.update(1)
    g.update(1)
    g.update(1)
    g.update(1)
    g.update(1)
    g.update(1)
    g.update(1)
    g.update(1)
    g.update(1)
    g.update(1)
