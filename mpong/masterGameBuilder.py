import mpong.model


class MasterGameBuilder(object):
    games = {}
    players = {}

    def createPlayer(self, name):
        if name not in players.keys():
            players[name] = model.Player(name)
        else:
            raise cherrypy.HTTPError(400, 'Player %s already exists' % name)

    def createGame(self, gameId, creatorName, maxPlayers):
        if gameId not in games.keys():
            games[gameId] = model.MPongGame(gameId, maxPlayers)
            self.join(gameId, creatorName)
        else:
            raise cherrypy.HTTPError(400, 'Game already %d exists' % gameId)

    def join(self, gameId, name):
        if name in players.keys() and gameId in games.keys():
            games[gameId].joinPlayer(players[name])
        else:
            raise cherrypy.HTTPError(400, 'No game with id %s found' % gameId)

    def leave(self, gameId, name):
        if name in players.keys() and gameId in games.keys():
            games[gameId].leavePlayer(player[name])
        else:
            raise cherrypy.HTTPError(400, 'No game with id %s found' % gameId)

    def startGame(self, gameId):
        if gameId in games.keys() and games[gameId].maxPlayers == len(games[gameId].joinedPlayers):
            games[gameId].start()
        else:
            raise cherrypy.HTTPError(400, 'No game with id %s found or not enough players, who knows.' % gameId)

    def stopGame(self, gameId):
        if gameId in games.keys():
            games[gameId].stop()
            del games[gameId]
        else:
            raise cherrypy.HTTPError(400, 'No game with id %s found' % gameId)

    def setPlayerSpeed(self, playerName, speedY):
        """ Set player speed in y-direction."""
        if playerName in players.keys():
            players[playerName].velocity = model.Vector(0, float(speedY))
        else:
            raise cherrypy.HTTPError(400, 'No player %s found' % playerName)

    def gameState(self, gameId):
        if gameId in games.keys():
            return games[gameId].getState()
        else:
            raise cherrypy.HTTPError(404, 'No game with id %s found' % gameId)

masterGame = MasterGameBuilder()
