import cherrypy
import numpy as np

class PaddleHandler:
    exposed = True

    def __init__(self, players):
        self.players = players

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        """ str -> float """
        try:
            data = cherrypy.request.json
            requestedSpeed = float(data['speed'])
            playerName = cherrypy.session.get('name')
            if playerName is None:
               raise cherrypy.HTTPError(400, 'No player with name %s' % playerName)
            player = self.players[playerName]
            paddle = player['paddle']
            paddle.velocity = np.array((0., requestedSpeed))
            cherrypy.log('Set paddle velocity to {0:f}'.format(requestedSpeed))
            return {'currentSpeed': requestedSpeed}
        except KeyError as e:
            raise cherrypy.HTTPError('{}'.format(e))

