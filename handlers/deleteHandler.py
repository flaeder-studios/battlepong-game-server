#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from mpong.masterGameBuilder import masterGame
from handlers import GameHandler

class DeleteHandler:

    exposed = True

    def POST(self, gameId):

            masterGame.deleteGame(gameId)
            for g in GameHandler.games:
                if g['id'] == gameId:
                    GameHandler.games.remove(g)
                    break
            cherrypy.log('Delete game %s' % currentGame['id'])
