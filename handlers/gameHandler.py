
import cherrypy


class GameHandler:
    exposed = True

    def __init__(self, players, gameData):
        self.players = players
        self.gameData = gameData

    def getAllGames(self):
        #games = cherrypy.engine.publish('mpong-get-all-games') #.pop()
        d = {}
        for gameID in self.gameData.keys():
            d[gameID] = self.getGame(gameID)
        return {'games': self.gameData}

    def getGame(self, gameID):
        game = cherrypy.engine.publish('mpong-get-game', gameID) #.pop()
        game = self.gameData[gameID]
        d = {}
        d['id'] = game['id']
        d['maxPlayers'] = game['maxPlayers']
        d['currentPlayers'] = game['currentPlayers']
        if 'activeGame' in game.keys():
            d['gameStarted'] = True
        return {'games': [d]}

    @cherrypy.tools.json_out()
    def GET(self, gameID=None):
        if not cherrypy.session.get('name'):
            raise cherrypy.HTTPError(401)
        if gameID is None:
            return self.getAllGames()
        else:
            return self.getGame(gameID)

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self, gameID=None):
        if not cherrypy.session.get('name'):
            raise cherrypy.HTTPError(401, 'name not set')
        playerName = cherrypy.session.get('name')
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
        game['gameStarted'] = False
        player = self.players[playerName]
        player['currentGame'] = game
        self.gameData[game['id']] = game
        cherrypy.log("GameHandler: created game %s" % game)
        return {'games': [game]}

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


