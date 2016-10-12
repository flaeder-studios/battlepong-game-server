import cherrypy
import mpong.model


class PlayerHandler:
    exposed = True

    def __init__(self, players):
        self.players = players

    @cherrypy.tools.json_out()
    def GET(self):
        if 'name' not in cherrypy.session:
            return {'player': {}}
        playerName = cherrypy.session['name']
        player = self.players[playerName]
        playerData = {}
        playerData['name'] = player['name']
        cherrypy.log("player: %s" % playerData)
        return {'player': playerData}

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        """ This method creates a player. A player name must be unique."""
        if 'name' in cherrypy.session:
            raise cherrypy.HTTPError('Player name already set. Cannot change player name.')
        data = cherrypy.request.json
        # if exists pull out player name from data
        if 'player' in data and 'name' in data['player']:
            playerName = data['player']['name']
            self.players[playerName] = {'name': playerName, 'currentGame': None, 'paddle': mpong.model.Paddle()}
            cherrypy.session['name'] = playerName
            cherrypy.log("set name to %s" % (playerName))
        return self.GET()
