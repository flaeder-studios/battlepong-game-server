#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy

class LeaveGameHandler:
    exposed = True

    def __init__(self, players, gameData):
        self.players = players
        self.gameData = gameData

    @cherrypy.tools.json_out()
    def POST(self):
        playerName = cherrypy.session.get('name')
        player = self.players[playerName]
        currentGame = player['currentGame']
        currentGame['currentPlayers'].remove(player)
        player['currentGame'] = None
        cherrypy.session['currentGame'] = None
        cherrypy.log("LeaveGameHandler: Player %s left game %s" % (playerName, currentGame))
        return {'games': [currentGame]}

