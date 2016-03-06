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
        if playerName in currentGame['joinedPlayers']:
            masterGame.leave(currentGame['id'], playerName)
            currentGame['joinedPlayers'].remove(playerName)
        cherrypy.session['currentGame'] = None
        
        return {'games': [currentGame]}

