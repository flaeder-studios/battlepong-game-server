import threading
import player
import model
import time

class MPongGame(threading.Thread):

    def __init__(self, id, maxPlayers):
        self.joinedPlayers = []
        self.id = id
        self.maxPlayers = maxPlayers
        self.gameStarted = False
        self.gameStopped = False
        self.model = None
        self.pt = None

    def join(self, newPlayer):
        if newPlayer not in self.joinedPlayers:
            self.joinedPlayers.append(newPlayer)
            return newPlayer

    def leave(self, leavingPlayer):
        for p in self.joinedPlayers:
            if p == leavingPlayer:
                del p
                return p

    def run(self):
        self.model = model.Game(100, self.joinedPlayers[0].name, self.joinedPlayers[1].name, 3)
        self.gameStarted = True
        self.pt = time.time()

        while True
            t = time.time()
            speed = {}
            speed['player1'] = model.Vector(player1.speed[0], player1.speed[1])
            speed['player2'] = model.Vector(player2.speed[0], player2.speed[1])
            self.model.update(speed)

    def stop(self):
        self.gameStopped = True

    def getState(self):
        pass


