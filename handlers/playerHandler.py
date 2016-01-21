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
            
        if 'currentGame' in cherrypy.session and cherrypy.session['currentGame']:
            player['currentGame'] = cherrypy.session['currentGame']
        
        player['createdGames'] = []
        
        cherrypy.log(str(player))
        
        return { 'player': player }
            
            
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        data = cherrypy.request.json
        
        if 'player' in data:
            data = data['player']
        
        if 'name' in data:
            cherrypy.session['name'] = data['name']
            
        cherrypy.log("set name to %s" % data['name'])
        
        return self.GET()
        