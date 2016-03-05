import model


class MasterGameBuilder(object):
    games = {}
    players = {}

    def createPlayer(self, name):
        if name not in players.keys():
            players[name] = model.Player(name)

    def createGame(self, gameID, creatorName, maxPlayers):
        if gameID not in games.keys():
            games[gameID] = model.MpongGame(gameID, maxPlayers)
            self.join(gameID, creatorName)

    def join(self, gameID, name):
        if name in players.keys() and gameID in games.keys():
            games[gameID].joinPlayer(players[name])

    def leave(self, gameID, name):
        if name in players.keys() and gameID in games.keys():
            games[gameID].leavePlayer(player[name])

    def startGame(self, gameID):
        if gameID in games.keys():
            games[gameID].start()

    def stopGame(self, gameID):
        if gameID in games.keys():
            games[gameID].stop()
            del games[gameID]

    def setPlayerSpeed(self, playerName, speedY):
        """ Set player speed in y-direction."""
        players[playerName].velocity = model.Vector(0, float(speedY))

    def gameState(self, gameID):
        if gameID in games.keys():
            return games[gameID].getState()
        else:
            return None

masterGame = MasterGameBuilder()
