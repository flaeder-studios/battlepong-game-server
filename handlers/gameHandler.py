import cherrypy
import handlers.handlerOutput


class GameHandler(handlers.handlerOutput.GetGameData):

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self, gameID=None):
        """Create a dict with game info. {id, maxPlayers, currentPlayers, activeGame}."""
        if not cherrypy.session.get('name'):
            raise cherrypy.HTTPError(401, 'name not set')
        playerName = cherrypy.session.get('name')
        player = self.players[playerName]
        game = cherrypy.request.json
        if 'id' not in game:
            if gameID:
                game['id'] = gameID
            else:
                raise cherrypy.HTTPError(400, 'game id not set')
        if 'maxPlayers' not in game:
            raise cherrypy.HTTPError(400, 'game maxPlayers not set')
        game['maxPlayers'] = int(game['maxPlayers'])
        game['currentPlayers'] = [player]
        game['activeGame'] = False
        player['currentGame'] = game
        self.gameData[game['id']] = game
        gameData = self.GET()
        cherrypy.log('games: {}'.format(gameData))
        return gameData

    @cherrypy.tools.json_out()
    def DELETE(self, gameID):
        if not cherrypy.session.get('name'):
            raise cherrypy.HTTPError(401, 'name not set')
        try:
            removedGame = self.gameData[gameID]
            del self.gameData[gameID]
            return {'games': [removedGame]}
        except KeyError as e:
            raise cherrypy.HTTPError('No game with id {}'.format(e))


