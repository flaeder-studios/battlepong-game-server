#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from mpong.masterGameBuilder import masterGame


class JoinGameHandler:
    exposed = True

    def GET(self, gameID):
        playerName = cherrypy.session.get('name')
        return "%s has joined game %s" % (playerName, gameID)

    @cherrypy.tools.json_out()
    def POST(self, gameID):

        # Add player to game. This allows him to pick up a websocket to the game. Return adress to ws.
        playerName = cherrypy.session.get('name')

        cherrypy.session['currentGame'] = masterGame.join(gameID, playerName)

        cherrypy.log("Player %s joined game %s" %(playerName, gameID))
        return {'games': [cherrypy.session['currentGame']]}

