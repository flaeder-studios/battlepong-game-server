import time
import threading
from handlers.gameHandler import GameHandler
import mpong.masterGameBuilder
from mpong.masterGameBuilder import masterGame
import cherrypy


class ControlUnit(threading.Thread):
    deleteGames = []
    deletePlayers = []

    def __init__(self, mgb):
        super(ControlUnit, self).__init__(target=self.run)
        self.mgb = mgb
        self.daemon = True

    def run(self):
        while True:
            time.sleep(10)
            pt = time.time()
            for gameId, value in mpong.masterGameBuilder.MasterGameBuilder.games.items():
                startTime = value[1]
                if pt - startTime > 10 and not len(value[0].joinedPlayers) > 0:
                    cherrypy.log('200','ControlUnit: game %s timeout' % gameId)
                    ControlUnit.deleteGames.append(gameId)
                    for g in GameHandler.games:
                        if g['id'] == gameId:
                            GameHandler.games.remove(g)
                            break
            for gameId in ControlUnit.deleteGames:
                self.mgb.deleteGame(gameId)
            for playerName, value in mpong.masterGameBuilder.MasterGameBuilder.players.items():
                startTime = value[1]
                if pt - startTime > 3000:
                    cherrypy.log('200','ControlUnit: player %s timeout' % playerName)
                    ControlUnit.deletePlayers.append(playerName)
            for playerName in ControlUnit.deletePlayers:
                self.mgb.deletePlayer(playerName)
            ControlUnit.deletePlayers = []
            ControlUnit.deleteGames = []


cu = ControlUnit(masterGame)
