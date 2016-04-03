#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from mpong.masterGameBuilder import masterGame


class StartHandler:

    exposed = True

    @cherrypy.tools.json_out()
    def POST(self):

        currentSessionGameId = cherrypy.session.get('currentGame')['id']
        currentGame = masterGame.getMetadata(currentSessionGameId)
        if not currentGame['gameStarted']:
            masterGame.startGame(currentSessionGameId)
            cherrypy.session['currentGame'] = masterGame.getMetadata(currentSessionGameId)
            currentGame = masterGame.getMetadata(currentSessionGameId)
            cherrypy.log('Start game %s' % currentGame)

        return currentGame
