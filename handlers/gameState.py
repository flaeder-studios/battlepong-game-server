import cherrypy


class GameState:
    exposed = True

    def __init__(self, gameData):
        self.gameData = gameData

    @cherrypy.tools.json_out()
    def GET(self, gameID):
        try:
            game = self.gameData[gameID]
            activeGame = game['activeGame']
            d = {}
            d['leftPaddle'] = {}
            d['leftPaddle']['position']     = (activeGame.leftPaddle.position[0], activeGame.leftPaddle.position[1])
            d['leftPaddle']['velocity']     = (activeGame.leftPaddle.velocity[0], activeGame.leftPaddle.velocity[1])
            d['leftPaddle']['dimensions']   = (activeGame.leftPaddle.dimensions[0], activeGame.leftPaddle.dimensions[1])
            d['leftPaddle']['name'] = game['currentPlayers'][0]['name']

            d['rightPaddle'] = {}
            d['rightPaddle']['position']    = (activeGame.rightPaddle.position[0], activeGame.rightPaddle.position[1])
            d['rightPaddle']['velocity']    = (activeGame.rightPaddle.velocity[0], activeGame.rightPaddle.velocity[1])
            d['rightPaddle']['dimensions']  = (activeGame.rightPaddle.dimensions[0], activeGame.rightPaddle.dimensions[1])
            d['rightPaddle']['name'] = game['currentPlayers'][1]['name']


            d['ball'] = {}
            d['ball']['position']   = (activeGame.ball.position[0], activeGame.ball.position[1])
            d['ball']['radius']     = activeGame.ball.radius
            d['ball']['speed']      = activeGame.ball.speed

            d['game'] = {}
            d['game']['center'] = (activeGame.gameCenter[0], activeGame.gameCenter[1])
            d['game']['dimensions'] = (activeGame.gameDimensions[0], activeGame.gameDimensions[1])

            return d
        except KeyError as e:
            raise cherrypy.HTTPError(400, 'gameState not set')