import cherrypy


class HandlerOutput:
    exposed = True

    def __init__(self, players, gameData):
        self.players = players
        self.gameData = gameData


class GetGameData(HandlerOutput):

    @cherrypy.tools.json_out()
    def GET(self, gameID=None):
        """Return gamedata for gameID. Gamedata is game id, current players, maxplayers, active game."""
        if gameID is not None:
            return self.helpGet(gameID)
        else:
            d = {}
            for key in self.gameData:
                d[key] = self.helpGet(key)[key]
            return d

    def helpGet(self, gameID):
        gameData = self.gameData[gameID]
        d = {}
        d['maxPlayers'] = gameData['maxPlayers']
        d['id'] = gameData['id']
        if gameData['activeGame']:
            d['activeGame'] = True
        else:
            d['activeGame'] = False
        d['currentPlayers'] = []
        for player in gameData['currentPlayers']:
            d['currentPlayers'].append(player['name'])
        return {gameID: d}