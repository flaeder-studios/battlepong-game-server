
# dimensions of gameboard. Values for halfGameboard is good to have
gameboard = {'hight': 3*2*6*50., 'width': 3*3*2*6*50.}
halfGameboard = {'hight': gameboard['hight'] / 2.0, 'width': gameboard['width'] / 2.0}

# player1, player2 and a ball. Position is at middle of object.
player1 = dict(name='Clint', points=0,
                            position=[halfGameboard['width'] - 250., -halfGameboard['hight']],
                            speed=[0., 0.],
                            width=gameboard['hight']/(6*3), hight=gameboard['hight']/6)
player2 = dict(name='Arnold', points=0,
                            position=[halfGameboard['width'] + 250, -halfGameboard['hight']],
                            speed=[0., 0.],
                            width=gameboard['hight']/(6*3), hight=gameboard['hight']/6)
ball = dict(position=[halfGameboard['width'], -halfGameboard['hight']],
                            speed=[1., 1.],
                            width=gameboard['hight']/12, hight=gameboard['hight']/12)

# collision detection for 'slow' moving objects. Gameboard coordinate (0, 0) is at upper left corner
def ball_collision(ball, player1, player2):
    position = ball['position']
    # check if ball bounces off roof or floor
    if position[1] > 0 - ball['hight']/2.:
        position[1] = -position[1]
    elif position[1] < -gameboard['hight'] + ball['hight']/2.:
        position[1] = -position[1]
    # check if ball hits a player
    if position[0] < player1['position'][0]:
        pos_y = player1['position'][1]
        if position[1] < pos_y + player1['hight']/2 and position[1] > pos_y - player1['hight']/2:
            position[0] = -position[0]
        else:
            player2['points'] += 1
            position[0] = halfGameboard['width']
            position[1] = -halfGameboard['hight']
    elif position[0] > player2['position'][0]:
        pos_y = player2['position'][1]
        if position[1] < pos_y + player2['hight']/2 and position[1] > pos_y - player2['hight']/2:
            position[0] = -position[0]
        else:
            player1['points'] += 1
            position[0] = halfGameboard['width']
            position[1] = -halfGameboard['hight']
    else:
        pass

# a player should not move outside the gameboard
def player_collision(player):
    position = player['position']
    if position[1] > 0 - player['hight']/2.:
        position[1] = 0 - player['hight']/2.    # highest possible position
    elif position[1] < -gameboard['hight'] + player['hight']/2.:
        position[1] = -gameboard['hight'] + player['hight']/2.  # lowest possible position


class Game(object):
    def __init__(self, player1_name, player2_name):
        self.gameBoard = gameboard
        self.halfGameBoard = halfGameboard
        self.player1 = player1
        self.player2 = player2
        self.ball = ball
        player1['name'] = player1_name
        player2['name'] = player2_name

    def printaut(self):
        print self.player1, self.player2, self.ball

if __name__ == '__main__':
    g = Game('Clint', 'Arnold')
    g.printaut()
