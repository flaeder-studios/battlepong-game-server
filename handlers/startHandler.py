#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
import numpy as np
import time
import threading
import mpong.model


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


class StartHandler:
    exposed = True

    def __init__(self, players):
        self.players = players

    @cherrypy.tools.json_out()
    def POST(self):
        playerName = cherrypy.session.get('name')
        player = self.players[playerName]
        currentGame = player['currentGame']
        cherrypy.session['currentGame'] = currentGame
        cherrypy.log('StartHandler: Start game %s' % game)
        players = currentGame['currentPlayers']
        currentGame['activeGame'] = ActiveGame(players[0]['paddle'], players[1]['paddle'])
        currentGame['activeGame'].start()
        return {'games': [currentGame] }
