#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from mpong.masterGameBuilder import masterGame

class LeaveGameHandler:
    
    exposed = True
    
    @cherrypy.tools.json_out()
    def POST(self):
        playerName = cherrypy.session.get('name')
        currentGame = cherrypy.session.get('currentGame')
        masterGame.leave(currentGame['id'], playerName)
        if playerName in currentGame['joinedPlayers']:
            currentGame['joinedPlayers'].remove(playerName)
        cherrypy.session['currentGame'] = None
        
        return {'games': [currentGame]}

