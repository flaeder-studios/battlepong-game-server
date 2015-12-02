
# dimensions of gameboard. Values for halfGameboard is good to have
gameboard = {'hight': 900., 'width': 1.6*900}
halfGameboard = {'hight': gameboard['hight'] / 2., 'width': gameboard['width'] / 2.}


# create classes for left player, right player and ball object.
class Paddle(object):
    def __init__(self, start_position):
        self.position = start_position
        self.speed = [0., 0.]
        self.hight = gameboard['hight']/(6.)
        self.width = gameboard['hight']/(6*3.)

    def __str__(self):
        return 'position: ' + str(self.position) + 'speed: ' + str(self.speed) + ', hight: %f, width: %f' % (self.hight, self.width)


class LeftPlayer(Paddle):
    def __init__(self, name):
        super(LeftPlayer, self).__init__([halfGameboard['width'] - 250., -halfGameboard['hight']])
        self.name = name

    def __str__(self):
        return Paddle.__str__(self) + ', name: %s' % (self.name)


class RightPlayer(Paddle):
    def __init__(self, name):
        super(RightPlayer, self).__init__([halfGameboard['width'] + 250., -halfGameboard['hight']])
        self.name = name

    def __str__(self):
        return Paddle.__str__(self) + ', name: %s' % (self.name)


class Ball(object):
    def __init__(self):
        self.position = [halfGameboard['width'], -halfGameboard['hight']]
        self.speed = [1., 1.]
        self.hight = gameboard['hight']/12.
        self.width = gameboard['hight']/12. 

    def __str__(self):
        return 'position: ' + str(self.position) + ', speed: ' + str(self.speed) + ', hight: %f, width: %f' % (self.hight, self.width)


# create Game. Contains players, ball and rules
class Game(object):
    def __init__(self, left_player_name, right_player_name):
        self.left_player = LeftPlayer(left_player_name)
        self.right_player = RightPlayer(right_player_name)
        self.ball = Ball()

    # a player should not move outside the gameboard
    def player_collision(player):
        position = player.position
        if position[1] > 0 - player.hight/2.:
            position[1] = 0 - player.hight/2.    # highest possible position
        elif position[1] < -gameboard['hight'] + player.hight/2.:
            position[1] = -gameboard['hight'] + player.hight/2.  # lowest possible position

    # collision detection for 'slow' moving objects. Gameboard coordinate (0, 0) is at upper left corner
    def ball_collision(ball, left_player, right_player):
        position = ball.position
        # check if ball bounces off roof or floor
        if position[1] > 0 - ball['hight']/2.:
            position[1] = -position[1]
        elif position[1] < -gameboard['hight'] + ball['hight']/2.:
            position[1] = -position[1]
        # check if ball hits player_left or player_right
        if position[0] < left_player.position[0]:
            pos_y = left_player.position[1]
            if position[1] < pos_y + left_player.hight/2. and position[1] > pos_y - left_player.hight/2.:
                position[0] = -position[0]
            else:
                right_player.points += 1
                position[0] = halfGameboard['width']
                position[1] = -halfGameboard['hight']
        elif position[0] > right_player.position[0]:
            pos_y = right_player.position[1]
            if position[1] < pos_y + right_player.hight/2. and position[1] > pos_y - right_player.hight/2.:
                position[0] = -position[0]
            else:
                left_player.points += 1
                position[0] = halfGameboard['width']
                position[1] = -halfGameboard['hight']
        else:
            pass

    # get player speeds from view.
    def update(self, left_player_speed, right_player_speed):
        pass

    def printaut(self):
        print 'left player:', '{', self.left_player, '}'
        print 'right player:', '{', self.right_player, '}'
        print'ball:', self.ball


if __name__ == '__main__':
    g = Game('Clint', 'Arnold')
    g.printaut()
