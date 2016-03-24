import pongsession
import names
import time


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
        while len(currentGame['joinedPlayers']) < currentGame['maxPlayers']:
            print '%d / %d' % (len(currentGame['joinedPlayers']), currentGame['maxPlayers'])
            time.sleep(1.0)
            player = s.getPlayer()['player']
            currentGame = player['currentGame']

        if currentGame['createdBy'] == self.name:
            s.startGame()
        else:
            return

        while not self.quit:
            state = s.getState(currentGame['id'])
            print state
            break








