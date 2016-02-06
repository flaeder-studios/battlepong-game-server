#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy

class PlayerHandler:
    
    exposed = True
    
    @cherrypy.tools.json_out()
    def GET(self):
        player = {}
        
        if 'name' in cherrypy.session:
            player['name'] = cherrypy.session['name']
        else:
            raise cherrypy.HTTPError(401, 'player name not set')
        
        cherrypy.log(str(player))
        
        return { 'player': player }
            
            
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        """ This method creates a player. A player name must be unique.'
        only one game can be created per name."""

        data = cherrypy.request.json

        if 'player' in data and 'name' in data['player']:
            playerName = str(data['player']['name'])
        else:
            raise cherrypy.HTTPError(401, 'player name not found')

        for g in GameHandler.games:
            if g['createdBy'] == playerName:
                raise cherrypy.HTTPError(401, 'player name not set')
        
        cherrypy.session['name'] = playerName

        cherrypy.log("set name to %s" % (playerName))
        
        return self.GET()
