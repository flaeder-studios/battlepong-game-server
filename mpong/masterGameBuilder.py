import model
import cherrypy


class MasterGameBuilder(object):
    games = {}
    players = {}

    def createPlayer(self, name):
        if name not in MasterGameBuilder.players.keys():
            MasterGameBuilder.players[name] = model.Player(name)
        else:
            raise cherrypy.HTTPError(400, 'MasterGameBuilder: Player %s already exists' % name)

    def createGame(self, gameId, maxPlayers):
        if gameId not in MasterGameBuilder.games.keys():
            MasterGameBuilder.games[gameId] = model.MPongGame(gameId, maxPlayers)
        else:
            raise cherrypy.HTTPError(400, 'MasterGameBuilder: Game already %s exists' % gameId)

    def join(self, gameId, name):
        if name in MasterGameBuilder.players.keys() and gameId in MasterGameBuilder.games.keys():
            MasterGameBuilder.games[gameId].joinPlayer(MasterGameBuilder.players[name])
        else:
            raise cherrypy.HTTPError(400, 'MasterGameBuilder: No game with id %s found' % gameId)

    def leave(self, gameId, name):
        if name in MasterGameBuilder.players.keys() and gameId in MasterGameBuilder.games.keys():
            MasterGameBuilder.games[gameId].leavePlayer(MasterGameBuilder.players[name])
        else:
            raise cherrypy.HTTPError(400, 'MasterGameBuilder: No game with id %s found' % gameId)

    def startGame(self, gameId):
        if gameId in MasterGameBuilder.games.keys() and MasterGameBuilder.games[gameId].maxPlayers == len(MasterGameBuilder.games[gameId].joinedPlayers):
            MasterGameBuilder.games[gameId].start()
        else:
            raise cherrypy.HTTPError(400, 'MasterGameBuilder: No game with id %s found or not enough joined players, who knows.' % gameId)

    def stopGame(self, gameId):
        if gameId in MasterGameBuilder.games:
            MasterGameBuilder.games[gameId].stop()
            del MasterGameBuilder.games[gameId]
        else:
            raise cherrypy.HTTPError(400, 'MasterGameBuilder: No game with id %s found' % gameId)

    def deleteGame(self, gameId):
        if gameId in MasterGameBuilder.games.keys() and not MasterGameBuilder.games[gameId].isAlive():
            del MasterGameBuilder.games[gameId]
        else:
            raise cherrypy.HTTPError(400, 'MasterGameBuilder: Cannot delete active game %s ' % gameId)

    def setPlayerSpeed(self, playerName, speedY):
        """ Set player speed in y-direction."""
        if playerName in MasterGameBuilder.players.keys():
            MasterGameBuilder.players[playerName].velocity = model.Vector(0, float(speedY))
        else:
            raise cherrypy.HTTPError(400, 'MasterGameBuilder: No player %s found' % playerName)

    def gameState(self, gameId):
        if gameId in MasterGameBuilder.games.keys():
            return MasterGameBuilder.games[gameId].getState()
        else:
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: No game with id %s found' % gameId)

masterGame = MasterGameBuilder()
masterGame.createPlayer('Arnold')
