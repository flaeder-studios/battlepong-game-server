class Player:
    def __init__(self):
        self.name = ''
        self.speed = [0, 0]

    def changeName(self, name):
        if name:
            self.name = name

