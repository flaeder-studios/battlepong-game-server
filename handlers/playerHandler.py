#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy

class PlayerHandler:
    
    exposed = True
    
    players = []

    @cherrypy.tools.json_out()
    def GET(self):
        player = {}

        if 'name' in cherrypy.session:
            player['name'] = cherrypy.session['name']

        if 'currentGame' in cherrypy.session and cherrypy.session['currentGame']:
            player['currentGame'] = cherrypy.session['currentGame']

        cherrypy.session['createdGames'] = []

        cherrypy.log(str(player))
        
        return { 'player': player }

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        """ This method creates a player. A player name must be unique."""

        data = cherrypy.request.json

        # if exists pull out player name from data
        if 'player' in data and 'name' in data['player']:
            playerName = str(data['player']['name'])
            if playerName in PlayerHandler.players:
                raise cherrypy.HTTPError(401, 'Player name %s not unique' % (playerName))
            cherrypy.session['name'] = playerName

        cherrypy.log("set name to %s" % (playerName))
        
        return self.GET()
