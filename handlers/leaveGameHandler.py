#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy

class LeaveGameHandler:
    
    exposed = True
    
    @cherrypy.tools.json_out()
    def POST(self):
        playerName = cherrypy.session.get('name')
        
        currentGame = cherrypy.session.get('currentGame')
        currentGame['joinedPlayers'].remove(playerName)
        cherrypy.session['currentGame'] = None
        
        #game = cherrypy.engine.publish('mpong-leave-game', gameId, playerName).pop()
        
        return {'games': [currentGame]}

