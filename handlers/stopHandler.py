#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from gameHandler import GameHandler
from mpong.masterGameBuilder import masterGame


class StopHandler:

    exposed = True

    def POST(self):

        playerName = cherrypy.session.get('name')
        player = masterGame.players[playerName][0]
        currentGame = player.getCurrentGame()
        stopGame = masterGame.stopGame(currentGame['id'])
        player.setCurrentGame(None)
        cherrypy.session['currentGame'] = player.getCurrentGame()

        cherrypy.log('Stop game %s' % stopGame['id'])
        return {'games':[stopGame]}


