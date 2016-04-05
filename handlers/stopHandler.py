#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from gameHandler import GameHandler
from mpong.masterGameBuilder import masterGame


class StopHandler:

    exposed = True

    def POST(self):

        currentGame = cherrypy.session.get('currentGame')
        stopGame = masterGame.stopGame(currentGame['id'])
        cherrypy.log('Stop game %s' % currentGame)
        return {'games':[currentGame]}
