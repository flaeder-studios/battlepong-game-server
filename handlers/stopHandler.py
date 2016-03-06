#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from mpong.masterGameBuilder import masterGame


class StopHandler:

    exposed = True

    def POST(self):

        currentGame = cherrypy.session.get('currentGame')
        if currentGame['gameStarted']:
            currentGame['gameStarted'] = False
            masterGame.stopGame(currentGame['id'])
            cherrypy.log('Stop game %s' % currentGame['id'])


