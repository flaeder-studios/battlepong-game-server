#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy

class PlayerHandler:
    
    exposed = True
    
    @cherrypy.tools.json_out()
    def GET(self):
        player = {}
        
        if 'playerName' in cherrypy.session:
            player['playerName'] = cherrypy.session['playerName']
        else:
            player['playerName'] = ''
            
        if 'currentGame' in cherrypy.session:
            player['currentGame'] = cherrypy.session['currentGame']
        else:
            player['currentGame'] = ''
        
        player['createdGames'] = []
        
        return { 'player': player }
            
            
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        data = cherrypy.request.json
        
        if 'player' in data:
            data = data['player']
        
        if 'playerName' in data:
            cherrypy.session['playerName'] = data['playerName']
        
        return self.GET()
        