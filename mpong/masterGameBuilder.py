import model
import cherrypy
import time
import threading

class MasterGameBuilder(object):
    games = {}
    players = {}

    def createPlayer(self, name):
        if name in MasterGameBuilder.games:
            raise cherrypy.HTTPError(400, 'MasterGameBuilder: Player %s already exists' % name)
        if name == "":
            raise cherrypy.HTTPError(403, 'MasterGameBuilder: Player name "" illegale')
        cherrypy.log('200','MasterGameBuilder: create player %s' % name)
        MasterGameBuilder.players[name] = [model.Player(name), time.time()]

    def createGame(self, gameId, maxPlayers):
        if gameId == "":
            raise cherrypy.HTTPError(403, 'MasterGameBuilder: Game name "" illegale')
        if gameId in MasterGameBuilder.games:
            raise cherrypy.HTTPError(400, 'MasterGameBuilder: Game already %s exists' % gameId)
        cherrypy.log('200','MasterGameBuilder: create game %s' % gameId)
        MasterGameBuilder.games[gameId] = [model.MPongGame(gameId, maxPlayers), time.time()]

    def join(self, gameId, name):
        if name not in MasterGameBuilder.players:
            raise cherrypy.HTTPError(401, 'MasterGameBuilder: No name %s found.' % (name))
        if gameId not in MasterGameBuilder.games:
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: No game with id %s found.' % (gameId))
        cherrypy.log('200','MasterGameBuilder: player %s joined game %s' % (name, gameId))
        MasterGameBuilder.players[name][1] = time.time()
        MasterGameBuilder.games[gameId][0].joinPlayer(MasterGameBuilder.players[name][0])

    def leave(self, gameId, name):
        if name not in MasterGameBuilder.players:
            raise cherrypy.HTTPError(401, 'MasterGameBuilder: No name %s found.' % name)
        if gameId not in MasterGameBuilder.games:
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: No game with id %s found.' % gameId)
        cherrypy.log('200','MasterGameBuilder: player %s left game %s' % (name, gameId))
        MasterGameBuilder.players[name][1] = time.time()
        MasterGameBuilder.games[gameId][1] = time.time()
        MasterGameBuilder.games[gameId][0].leavePlayer(MasterGameBuilder.players[name][0])

    def startGame(self, gameId):
        if gameId not in MasterGameBuilder.games:
            raise cherrypy.HTTPError(401, 'MasterGameBuilder: No game with id %s found' % gameId)
        if not MasterGameBuilder.games[gameId][0].maxPlayers == len(MasterGameBuilder.games[gameId][0].joinedPlayers):
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: Not enough players joined')
        cherrypy.log('200','MasterGameBuilder: start game %s' % gameId)
        MasterGameBuilder.games[gameId][0].start()

    def stopGame(self, gameId):
        if gameId not in MasterGameBuilder.games:
            raise cherrypy.HTTPError(400, 'MasterGameBuilder: No game with id %s found' % gameId)
        MasterGameBuilder.games[gameId][0].stop()
        cherrypy.log('200','MasterGameBuilder: stop and remove game %s' % gameId)
        del MasterGameBuilder.games[gameId]

    def setPlayerSpeed(self, playerName, speedY):
        """ Set player speed in y-direction."""
        if playerName not in MasterGameBuilder.players:
            raise cherrypy.HTTPError(401, 'MasterGameBuilder: No player %s found' % playerName)
        cherrypy.log('200','MasterGameBuilder: set player %s speed in y-direction to %f' % (playerName, speedY))
        MasterGameBuilder.players[playerName][1] = time.time()
        MasterGameBuilder.players[playerName][0].velocity = model.Vector(0, float(speedY))

    def gameState(self, gameId):
        if gameId not in MasterGameBuilder.games:
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: No game with id %s found' % gameId)
        cherrypy.log('200','MasterGameBuilder: game %s state %s' % (gameId, MasterGameBuilder.games[gameId][0].getState()))
        return MasterGameBuilder.games[gameId][0].getState()

    def deletePlayer(self, playerName):
        if playerName not in MasterGameBuilder.players:
            raise cherrypy.HTTPError(401, 'MasterGameBuilder: No player with name %s found' % playerName)
        cherrypy.log('200','MasterGameBuilder: delete player %s' % playerName)
        del MasterGameBuilder.players[playerName[0]]

    def deleteGame(self, gameId):
        if gameId not in MasterGameBuilder.games:
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: Game do not exist')
        if MasterGameBuilder.games[gameId][0].isAlive():
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: Cannot delete active game %s ' % gameId)
        cherrypy.log('200','MasterGameBuilder: delete game %s' % gameId)
        del MasterGameBuilder.games[gameId]


masterGame = MasterGameBuilder()
masterGame.createPlayer('Arnold')
