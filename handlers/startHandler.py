#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from mpong.masterGameBuilder import masterGame


class StartHandler:

    exposed = True

    @cherrypy.tools.json_out()
    def POST(self):

        currentSessionGameId = cherrypy.session.get('currentGame')['id']
        currentGame = masterGame.getGameData(currentSessionGameId)
        if not currentGame['gameStarted']:
            masterGame.startGame(currentSessionGameId)
            cherrypy.session['currentGame'] = masterGame.getGameData(currentSessionGameId)
            currentGame = masterGame.getGameData(currentSessionGameId)
            cherrypy.log('Start game %s' % currentGame)

        return currentGame
