import cherrypy
import handlers.handlerOutput

class LeaveGameHandler(handlers.handlerOutput.GetGameData):

    @cherrypy.tools.json_out()
    def POST(self):
        try:
            playerName = cherrypy.session.get('name')
            player = self.players[playerName]
            currentGame = player['currentGame']
            if currentGame is not None:
                currentGame['currentPlayers'].remove(player)
                player['currentGame'] = None
                cherrypy.session['currentGame'] = None
                cherrypy.log("LeaveGameHandler: Player %s left game %s" % (playerName, currentGame))
            return self.GET()
        except KeyError as e:
            raise cherrypy.HTTPError('{}'.format(e))