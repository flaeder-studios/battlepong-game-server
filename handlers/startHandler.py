import cherrypy
import numpy as np
import time
import threading
import mpong.model
import handlers.handlerOutput


class ActiveGame(threading.Thread):
    def __init__(self, leftPaddle, rightPaddle):
        self.gameCenter = np.array((0., 0.))
        self.gameDimensions = np.array((500., 500 / 3.))
        self.leftPaddle = leftPaddle
        self.rightPaddle = rightPaddle
        self.ball = mpong.model.Ball()
        self.daemon = True
        self.stopped = False

    def run(self):
        game = mpong.model.Game(self.gameCenter, self.gameDimensions, self.leftPaddle, self.rightPaddle, self.ball)
        tp = time.time()
        dt = 0
        while not self.stopped:
            self.ball.position = self.ball.position + self.ball.velocity * dt
            self.leftPaddle.position = self.leftPaddle.position + self.leftPaddle.velocity * dt
            self.rightPaddle.position = self.rightPaddle.position + self.rightPaddle.velocity * dt
            game.collision()
            dt = time.time() - tp
            tp = time.time()


class StartHandler(handlers.handlerOutput.GetGameData):

    @cherrypy.tools.json_out()
    def POST(self):
        playerName = cherrypy.session.get('name')
        if playerName is None:
            raise cherrypy.HTTPError('No player name in session.')
        try:
            player = self.players[playerName]
            currentGame = player['currentGame']
            cherrypy.session['currentGame'] = currentGame
            cherrypy.log('StartHandler: Start game {}'.format(currentGame['id']))
            players = currentGame['currentPlayers']
            currentGame['activeGame'] = ActiveGame(players[0]['paddle'], players[1]['paddle'])
            currentGame['activeGame'].start()
            return self.GET(currentGame['id'])
        except KeyError as e:
            raise cherrypy.HTTPError('startHandler: {}'.format(e))
