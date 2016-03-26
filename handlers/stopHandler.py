#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from gameHandler import GameHandler
from mpong.masterGameBuilder import masterGame


class StopHandler:

    exposed = True

    def POST(self):

        currentGame = cherrypy.session.get('currentGame')
        if currentGame['gameStarted']:
            currentGame['gameStarted'] = False
            for g in GameHandler.games:
                if g['id'] == currentGame['id']:
                    GameHandler.games.remove(g)
            masterGame.stopGame(currentGame['id'])
            cherrypy.session['currentGame'] = None

            cherrypy.log('Stop game %s' % currentGame['id'])


