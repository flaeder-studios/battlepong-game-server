import model
import cherrypy


class MasterGameBuilder(object):
    games = {}
    players = {}

    def createPlayer(self, name):
        if name not in MasterGameBuilder.players.keys():
            MasterGameBuilder.players[name] = model.Player(name)
        else:
            raise cherrypy.HTTPError(400, 'Player %s already exists' % name)

    def createGame(self, gameId, creatorName, maxPlayers):
        if gameId not in MasterGameBuilder.games.keys():
            MasterGameBuilder.games[gameId] = model.MPongGame(gameId, maxPlayers)
            self.join(gameId, creatorName)
        else:
            raise cherrypy.HTTPError(400, 'Game already %d exists' % gameId)

    def join(self, gameId, name):
        if name in MasterGameBuilder.players.keys() and gameId in MasterGameBuilder.games.keys():
            MasterGameBuilder.games[gameId].joinPlayer(MasterGameBuilder.players[name])
        else:
            raise cherrypy.HTTPError(400, 'No game with id %s found' % gameId)

    def leave(self, gameId, name):
        if name in MasterGameBuilder.players.keys() and gameId in MasterGameBuilder.games.keys():
            MasterGameBuilder.games[gameId].leavePlayer(MasterGameBuilder.player[name])
        else:
            raise cherrypy.HTTPError(400, 'No game with id %s found' % gameId)

    def startGame(self, gameId):
        if gameId in MasterGameBuilder.games.keys() and MasterGameBuilder.games[gameId].maxPlayers == len(MasterGameBuilder.games[gameId].joinedPlayers):
            MasterGameBuilder.games[gameId].start()
        else:
            raise cherrypy.HTTPError(400, 'No game with id %s found or not enough MasterGameBuilder.players, who knows.' % gameId)

    def stopGame(self, gameId):
        if gameId in MasterGameBuilder.games.keys():
            MasterGameBuilder.games[gameId].stop()
            del MasterGameBuilder.games[gameId]
        else:
            raise cherrypy.HTTPError(400, 'No game with id %s found' % gameId)

    def setPlayerSpeed(self, playerName, speedY):
        """ Set player speed in y-direction."""
        if playerName in MasterGameBuilder.players.keys():
            MasterGameBuilder.players[playerName].velocity = model.Vector(0, float(speedY))
        else:
            raise cherrypy.HTTPError(400, 'No player %s found' % playerName)

    def gameState(self, gameId):
        if gameId in MasterGameBuilder.games.keys():
            return MasterGameBuilder.games[gameId].getState()
        else:
            raise cherrypy.HTTPError(404, 'No game with id %s found' % gameId)

masterGame = MasterGameBuilder()
