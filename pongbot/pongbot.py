import pongsession
import names
import time

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
            print '%d / %d' % (len(currentGame['joinedPlayers']), currentGame['maxPlayers'])
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
        P = 0.25
        while not state['winner']:
            state = s.getState(currentGame['id'])
            t = time.time()

            # adjust paddle speed
            paddle = state['paddles'][name]
            ball = state['balls']['gameBall']

            if paddle['position'][0] < 0:
                if dot(ball['velocity'], [1, 0]) < 0:
                    poserr = paddle['position'][1] - paddle['position'][1]
                else:
                    poserr = -paddle['position'][1]
            else:
                if dot(ball['velocity'], [1, 0]) > 0:
                    poserr = paddle['position'][1] - paddle['position'][1]
                else:
                    poserr = -paddle['position'][1]

            dt = t - pt
            vref = poserr / dt
            verr = vref - paddle['velocity'][1]

            v = verr * P + ball['velocity'][1]
            s.setPaddleSpeed(v)


        print "game over! %s won" % state['winner']






