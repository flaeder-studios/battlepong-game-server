#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy


class StopHandler:
    exposed = True

    def __init__(self, players):
        self.players = players

    def POST(self):
        playerName = cherrypy.session.get('name')
        player = self.players[playerName]
        currentGame = player['currentGame']
        activeGame = currentGame['activeGame']
        activeGame.stopped = True
        cherrypy.log('StopHandler: stop game %s' % game)
        return {'games':[game]}
