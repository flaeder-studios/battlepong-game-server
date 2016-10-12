import cherrypy
import handlers.handlerOutput


class StopHandler(handlers.handlerOutput.GetGameData):

    def POST(self):
        playerName = cherrypy.session.get('name')
        if playerName is None:
            raise cherrypy.HTTPError('No player name in session.')
        try:
            player = self.players[playerName]
            currentGame = player['currentGame']
            activeGame = currentGame['activeGame']
            activeGame.stopped = True
            cherrypy.log('StopHandler: stop game {}'.format(currentGame['id']))
            return self.GET(currentGame['id'])
        except KeyError as e:
            raise cherrypy.HTTPError('stopHandler: {}'.format(e))
