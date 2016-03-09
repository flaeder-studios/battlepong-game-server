#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from mpong.masterGameBuilder import masterGame


class StartHandler:

    exposed = True

    def POST(self):

        currentGame = cherrypy.session.get('currentGame')
        if not currentGame['gameStarted']:
            currentGame['gameStarted'] = True
            masterGame.startGame(currentGame['id'])
            cherrypy.log('Start game %s' % currentGame['id'])
