#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from mpong.masterGameBuilder import masterGame


class PlayerHandler:
    
    exposed = True
    
    @cherrypy.tools.json_out()
    def GET(self):
        player = {}

        if 'name' not in cherrypy.session:
            return { 'player': {}}
        playerName = cherrypy.session['name']
        player = masterGame.players[playerName][0]
        cherrypy.session['currentGame'] = player.getCurrentGame()
        cherrypy.session['createdGames'] = player.getCreatedGames()
        cherrypy.session['createdGames'] = player.getCreatedGames()

        cherrypy.log("player: %s" % player.getPlayerData())
        return { 'player': player.getPlayerData() }

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        """ This method creates a player. A player name must be unique."""

        data = cherrypy.request.json

        # if exists pull out player name from data
        if 'player' in data and 'name' in data['player']:
            playerName = data['player']['name']
            masterGame.createPlayer(playerName)
            cherrypy.session['name'] = playerName

        cherrypy.log("set name to %s" % (playerName))
        
        return self.GET()
