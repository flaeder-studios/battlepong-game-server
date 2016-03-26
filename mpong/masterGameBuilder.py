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
        MasterGameBuilder.players[name] = [model.Player(name), time.time()]

    def createGame(self, gameId, maxPlayers):
        if gameId == "":
            raise cherrypy.HTTPError(403, 'MasterGameBuilder: Game name "" illegale')
        if gameId in MasterGameBuilder.games:
            raise cherrypy.HTTPError(400, 'MasterGameBuilder: Game already %s exists' % gameId)
        MasterGameBuilder.games[gameId] = [model.MPongGame(gameId, maxPlayers), time.time()]

    def join(self, gameId, name):
        if name not in MasterGameBuilder.players:
            raise cherrypy.HTTPError(401, 'MasterGameBuilder: No name %s found.' % (name))
        if gameId not in MasterGameBuilder.games:
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: No game with id %s found.' % (gameId))
        MasterGameBuilder.players[name][1] = time.time()
        MasterGameBuilder.games[gameId][1] = time.time()
        MasterGameBuilder.games[gameId][0].joinPlayer(MasterGameBuilder.players[name][0])

    def leave(self, gameId, name):
        if name not in MasterGameBuilder.players:
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: No name %s found.' % name)
        if gameId not in MasterGameBuilder.games:
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: No game with id %s found.' % gameId)
        MasterGameBuilder.players[name][1] = time.time()
        MasterGameBuilder.games[gameId][1] = time.time()
        MasterGameBuilder.games[gameId][0].leavePlayer(MasterGameBuilder.players[name][0])

    def startGame(self, gameId):
        if gameId not in MasterGameBuilder.games:
            raise cherrypy.HTTPError(400, 'MasterGameBuilder: No game with id %s found' % gameId)
        if not MasterGameBuilder.games[gameId][0].maxPlayers == len(MasterGameBuilder.games[gameId][0].joinedPlayers):
            raise cherrypy.HTTPError(400, 'MasterGameBuilder: Not enough players joined')
        MasterGameBuilder.games[gameId][1] = time.time()
        MasterGameBuilder.games[gameId][0].start()

    def stopGame(self, gameId):
        if gameId not in MasterGameBuilder.games:
            raise cherrypy.HTTPError(400, 'MasterGameBuilder: No game with id %s found' % gameId)
        MasterGameBuilder.games[gameId][0].stop()
        del MasterGameBuilder.games[gameId]

    def setPlayerSpeed(self, playerName, speedY):
        """ Set player speed in y-direction."""
        if playerName not in MasterGameBuilder.players:
            raise cherrypy.HTTPError(400, 'MasterGameBuilder: No player %s found' % playerName)
        MasterGameBuilder.players[playerName][1] = time.time()
        MasterGameBuilder.players[playerName][0].velocity = model.Vector(0, float(speedY))

    def gameState(self, gameId):
        if gameId not in MasterGameBuilder.games:
            raise cherrypy.HTTPError(404, 'MasterGameBuilder: No game with id %s found' % gameId)
        MasterGameBuilder.games[gameId][1] = time.time()
        return MasterGameBuilder.games[gameId][0].getState()

    def deletePlayer(self, playerName):
        if playerName in MasterGameBuilder.players:
            del MasterGameBuilder.players[playerName[0]]
        else:
            raise cherrypy.HTTPError(400, 'MasterGameBuilder: No player with name %s found' % playerName)

    def deleteGame(self, gameId):
        if gameId in MasterGameBuilder.games and not MasterGameBuilder.games[gameId][0].isAlive():
            del MasterGameBuilder.games[gameId]
        else:
            raise cherrypy.HTTPError(400, 'MasterGameBuilder: Cannot delete active game %s ' % gameId)


class ControlUnit(threading.Thread):
    deleteGames = []
    deletePlayers = []

    def __init__(self, mgb):
        super(ControlUnit, self).__init__(target=self.run)
        self.mgb = mgb
        self.daemon = True

    def run(self):
        while True:
            time.sleep(20)
            pt = time.time()
            for gameId, value in MasterGameBuilder.games.items():
                startTime = value[1]
                if pt - startTime > 3600:
                    for s in cherrypy.session.cache.values():
                        self.clearSession(gameId, s)
                    ControlUnit.deleteGames.append(gameId)
            for gameId in ControlUnit.deleteGames:
                mgb.deleteGame(gameId)
            for playerName, value in MasterGameBuilder.players.items():
                startTime = value[1]
                if pt - startTime > 3600:
                    ControlUnit.deletePlayers.append(playerName)
            for playerName in ControlUnit.deletePlayers:
                mgb.deletePlayer(playerName)
            ControlUnit.deletePlayers = []
            ControlUnit.deleteGames = []

    def clearSession(self, gameId, session):
        createdGames = session['createdGames']
        deleteGame = None 
        if createdGames:
            for game in createdGames:
                if game[u'id'] == gameId:
                    deleteGame = game
                    break
        if deleteGame:
            createdGames.remove(deleteGame)
        currentGame = session['currentGame']
        deleteGame = None
        if currentGame:
            for game in currentGame:
                if game[u'id'] == gameId:
                    deleteGame = game
                    break
        if deleteGame:
            currentGame.remove(deleteGame)


masterGame = MasterGameBuilder()
cu = ControlUnit(masterGame)
cu.start()
masterGame.createPlayer('Arnold')
