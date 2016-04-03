import model
import cherrypy
import time
import threading

class MasterGameBuilder(object):

    def __init__(self):
        self.games = {}
        self.players = {}

    def createPlayer(self, name):
        if name in self.games:
            raise cherrypy.HTTPError(400, 'MasterGameBuilder: Player %s already exists' % name)
        if name == "":
            raise cherrypy.HTTPError(403, 'MasterGameBuilder: Player name "" illegale')
        cherrypy.log('200','MasterGameBuilder: create player %s' % name)
        self.players[name] = [model.Player(name), time.time()]

    def createGame(self, gameID, maxPlayers, createdBy):
        if gameID == "":
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: Game name "" illegale')
        if gameID in self.games:
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: Game already %s exists' % gameID)
        self.games[gameID] = [model.MPongGame(gameID, maxPlayers, createdBy), time.time()]
        if gameID == 'TerminatorConnan':
            self.join(gameID, 'Arnold')
        cherrypy.log('200','MasterGameBuilder: create game %s' % gameID)
        return self.getMetadata(gameID)

    def getMetadata(self, gameID):
        if gameID not in self.games:
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: No game with id %s found.' % (gameID))
        cherrypy.log('200', 'MasterGameBuilder: returning metadata for game %s' % gameID)
        return self.games[gameID][0].getMetadata()

    def getMetadataAll(self):
        return [value[0].getMetadata() for key, value in self.games.items()]

    def join(self, gameID, name):
        if name not in self.players:
            raise cherrypy.HTTPError(401, 'MasterGameBuilder: No name %s found.' % (name))
        if gameID not in self.games:
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: No game with id %s found.' % (gameID))
        self.players[name][1] = time.time()
        self.games[gameID][0].joinPlayer(self.players[name][0])
        for player in self.games[gameID][0].joinedPlayers:
            player.setCurrentGame(self.getMetadata(gameID))
        cherrypy.log('200','MasterGameBuilder: player %s joined game %s' % (name, gameID))
        return self.getMetadata(gameID)

    def leave(self, gameID, name):
        if name not in self.players:
            raise cherrypy.HTTPError(401, 'MasterGameBuilder: No name %s found.' % name)
        if gameID not in self.games:
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: No game with id %s found.' % gameID)
        cherrypy.log('200','MasterGameBuilder: player %s left game %s' % (name, gameID))
        self.players[name][1] = time.time()
        self.games[gameID][1] = time.time()
        self.games[gameID][0].leavePlayer(self.players[name][0])

    def startGame(self, gameID):
        if gameID not in self.games:
            raise cherrypy.HTTPError(401, 'MasterGameBuilder: No game with id %s found' % gameID)
        if not self.games[gameID][0].maxPlayers == len(self.games[gameID][0].joinedPlayers):
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: Not enough players joined')
        cherrypy.log('200','MasterGameBuilder: start game %s' % gameID)
        if self.games[gameID][0].getState()['gameStarted']:
            cherrypy.log("MasterGameBuilder: Game %s already started" % gameID)
        else:
            self.games[gameID][0].start()
            cherrypy.log("MasterGameBuilder: Starting game %s" % gameID)

    def stopGame(self, gameID):
        if gameID not in self.games:
            raise cherrypy.HTTPError(400, 'MasterGameBuilder: No game with id %s found' % gameID)
        self.games[gameID][0].stop()
        cherrypy.log('200','MasterGameBuilder: stop game %s' % gameID)
        return self.games[gameID][0].getMetadata()

    def setPlayerSpeed(self, playerName, speedY):
        """ Set player speed in y-direction."""
        if playerName not in self.players:
            raise cherrypy.HTTPError(401, 'MasterGameBuilder: No player %s found' % playerName)
        cherrypy.log('200','MasterGameBuilder: set player %s speed in y-direction to %f' % (playerName, speedY))
        self.players[playerName][1] = time.time()
        self.players[playerName][0].velocity = model.Vector(0, float(speedY))

    def gameState(self, gameID):
        if gameID not in self.games:
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: No game with id %s found' % gameID)
        cherrypy.log('200','MasterGameBuilder: game %s state %s' % (gameID, self.games[gameID][0].getState()))
        return self.games[gameID][0].getState()

    def deletePlayer(self, playerName):
        if playerName not in self.players:
            raise cherrypy.HTTPError(401, 'MasterGameBuilder: No player with name %s found' % playerName)
        cherrypy.log('200','MasterGameBuilder: delete player %s' % playerName)
        del self.players[playerName[0]]

    def deleteGame(self, gameID):
        if gameID not in self.games:
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: Game do not exist')
        if self.games[gameID][0].isAlive():
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: Cannot delete active game %s ' % gameID)
        cherrypy.log('200','MasterGameBuilder: delete game %s' % gameID)
        removedGame = self.getMetadata(gameID)
        del self.games[gameID]
        return removedGame


masterGame = MasterGameBuilder()
masterGame.createPlayer('Arnold')
