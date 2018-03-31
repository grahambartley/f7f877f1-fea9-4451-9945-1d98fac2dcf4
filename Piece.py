class Piece(object):
    def __init__(self, pieceName, position, player):
        self.color    = player.color
        self.pieceName = pieceName
        self.pos  = position
        self.noMoves = 0
    def __str__(self):
        if self.color is 'white':
            return self.pieceName.upper()
        else:
            return self.pieceName

    def canbepromoted(self):
        if str(self.pos[0]) in '07':
            return True

    def promote(self, to):
        self.pieceName = to.lower()