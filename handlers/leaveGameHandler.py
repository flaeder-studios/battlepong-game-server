#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from mpong.masterGameBuilder import masterGame

class LeaveGameHandler:
    
    exposed = True
    
    @cherrypy.tools.json_out()
    def POST(self):
        playerName = cherrypy.session.get('name')
        currentGame = masterGame.getCurrentGame(playerName)
        masterGame.leave(currentGame['id'], playerName)
        cherrypy.session['currentGame'] = masterGame.getCurrentGame(playerName)
        
        return {'games': [currentGame]}

