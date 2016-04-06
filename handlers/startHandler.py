#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from mpong.masterGameBuilder import masterGame


class StartHandler:

    exposed = True

    @cherrypy.tools.json_out()
    def POST(self):

        playerName = cherrypy.session.get('name')
        if not masterGame.getCurrentGame(playerName)['gameStarted']:
            masterGame.startGame(masterGame.getCurrentGame(playerName)['id'])
            cherrypy.session['currentGame'] = masterGame.getCurrentGame(playerName)
            cherrypy.log('Start game %s' % masterGame.getCurrentGame(playerName))

        return masterGame.getCurrentGame(playerName)
