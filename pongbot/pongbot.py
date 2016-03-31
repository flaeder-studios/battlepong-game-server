import pongsession
import names
import time
import math

def dot(x,y):
    return sum(p * q for (p, q) in zip(x,y))

class PongBot:

    def __init__(self):

        # set a default name
        self.name = names.get_last_name()
        self.quit = False

    def run(self):
        s = pongsession.PongSession('localhost', 8080)

        self.name = names.get_last_name()
        s.startSession()
        s.setName(self.name)

        games = s.getGames()

        for g in games['games']:
            if len(g['joinedPlayers']) < g['maxPlayers']:
                try:
                    s.joinGame(g['id'])
                    break
                except pongsession.RequestNotOk:
                    continue

        else:
            s.createGame(self.name, 2)
            s.joinGame(self.name)

        player = s.getPlayer()['player']
        currentGame = player['currentGame']
        name = player['name']
        while len(currentGame['joinedPlayers']) < currentGame['maxPlayers']:
            print 'waiting for oponent (%d / %d joined)' % (len(currentGame['joinedPlayers']), currentGame['maxPlayers'])
            time.sleep(1.0)
            player = s.getPlayer()['player']
            currentGame = player['currentGame']

        if currentGame['createdBy'] == self.name:
            print "starting game"
            s.startGame()

        state = s.getState(currentGame['id'])
        while state['gameStarted'] != 0:
            print "waiting for game to start... (%d)" % state['gameStarted']
            state = s.getState(currentGame['id'])
            time.sleep(1.0)

        print "here we go!"
        pt = time.time()
        P = 4
        while not state['winner']:
            state = s.getState(currentGame['id'])
            t = time.time()

            # adjust paddle speed
            paddle = state['paddles'][name]
            ball = state['balls']['gameBall']

            if (paddle['position'][0] < 0 and ball['velocity'][0] < 0) or (paddle['position'][0] > 0 and ball['velocity'][0] > 0):
                poserr = ball['position'][1] - paddle['position'][1]
            else:
                poserr = -paddle['position'][1]

            dt = t - pt
            vref = math.copysign(3, poserr)
            verr = vref - paddle['velocity'][1]

            v = verr * P * dt + ball['velocity'][1]
            s.setPaddleSpeed(poserr * P)


        print "game over! %s won" % state['winner']






