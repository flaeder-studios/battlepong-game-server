import cherrypy
import handlers.handlerOutput


class JoinGameHandler(handlers.handlerOutput.GetGameData):

    @cherrypy.tools.json_out()
    def POST(self, gameID):
        # Add player to game. This allows him to pick up a websocket to the game. Return adress to ws.
        try:
            playerName = cherrypy.session.get('name')
            player = self.players[playerName]
            game = self.gameData[gameID]
            if len(game['currentPlayers']) < 2:
                game['currentPlayers'].append(player)
                player['currentGame'] = game
            else:
                raise cherrypy.HTTPError('game is full of players.')
            return self.GET()
        except KeyError as e:
            raise cherrypy.HTTPError('No game with id {}'.format(e))
