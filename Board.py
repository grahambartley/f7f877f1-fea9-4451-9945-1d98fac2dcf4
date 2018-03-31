import Piece
import Player

class Board(object):
    def __init__(self, player1, player2):
        self.board = dict()
        for player in [player1, player2]:
            if player.color is 'white':
                aRow, bRow = 0, 1
                player.capRow = 4
            else:
                aRow, bRow = 7, 6
                player.capRow = 3

            [self.board.setdefault((bRow,x), Piece.Piece('p', (bRow,x), player)) \
            for x in range(8)]
            [self.board.setdefault((aRow,x), Piece.Piece('r', (aRow,x), player)) \
            for x in [0,7]]
            [self.board.setdefault((aRow,x), Piece.Piece('kn',(aRow,x), player)) \
            for x in [1,6]]
            [self.board.setdefault((aRow,x), Piece.Piece('b', (aRow,x), player)) \
            for x in [2,5]]
            self.board.setdefault((aRow,3),  Piece.Piece('q', (aRow,3), player))
            self.board.setdefault((aRow,4),  Piece.Piece('k', (aRow,4), player))

    def printBoard(self):
        tmp = ""
        print ("      a     b     c     d     e     f     g     h")
        for i in range(8):
            print ("   -------------------------------------------------")
            print (str(i + 1), end='')
            for j in range(8):
                if (i, j) not in self.board:
                    print (" | " + "   ", end='')
                else:
                    print (" |  %s " % self.board[(i, j)], end='')
            print (" |")
        print ("   -------------------------------------------------")
        print ("\n")

    def refreshScreen(self, player):
        if player.color is 'white':
            player1, player2 = player, player.opponent
        else:
            player1, player2 = player.opponent, player
        self.printBoard()

    def run(self, player):
        self.refreshScreen(player)
        while True:
            print (player.turn(self.board))
            try:
                start, target = player.getMove(self.board)
            except (IndexError, ValueError):
                self.refreshScreen(player)
                print ("\n\nThat move is not vaild.")
            except TypeError:
                break
            else:
                if target in self.board or self.board[start].pieceName is 'p':
                    Player.Player.moves = 0
                else:
                    Player.Player.moves += 1
                player.doMove(self.board, start, target)
                player.playedturns += 1
                if self.board[target].pieceName is 'p':
                    if self.board[target].canbepromoted():
                        player.canPromote(self.board, target)
                player = player.opponent
                if player.isDraw(self.board):
                    return 1, player
                elif player.isCheckMate(self.board):
                    return 2, player
                else:
                    self.refreshScreen(player)

    def end(self, player, result):
        loser = player.name
        win = player.opponent.name
        if result == 1:
            endstring = "\n{} and {} have tied".format(win, loser)
        elif result == 2:
            endstring = "\n{} put {} in checkmate.".format(win, loser)
        self.printBoard()
        return endstring