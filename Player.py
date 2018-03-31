class Player(object):
    allSpaces = [(x, y) for x in range(8) for y in range(8)]
    moves = 0
    def __init__(self, color, name):
        self.color   = color
        self.name     = name
        self.playedturns = 0
    def __str__(self):
        return self.name+' as '+self.color

    def setOpp(self, opponent):
        self.opponent = opponent

    def getPieces(self, board):
        return [pos for pos in board if board[pos].color is self.color]

    def potentialTargets(self, playerColour):
        return [pos for pos in self.allSpaces if pos not in playerColour]

    def kingPos(self, board):
        for my in self.getPieces(board):
            if board[my].pieceName is 'k':
                return my

    def possibleMoves(self, board):
        myPieces=self.getPieces(board)
        for my in myPieces:
            for target in self.potentialTargets(myPieces):
                if self.canMove(board, my, target):
                    if not self.makeCheck(my, target, board):
                        yield (my, target)

    def getPos(self, move):
        col  = int(ord(move[0].lower())-97)
        row  = int(move[1])-1
        colNext = int(ord(move[2].lower())-97)
        rowNext = int(move[3])-1
        start     = (row, col)
        target    = (rowNext, colNext)
        return start, target

    def isDraw(self, board):
        if not list(self.possibleMoves(board)) and not self.isCheck(board):
            return True
        if len(list(self.getPieces(board))) == \
           len(list(self.opponent.getPieces(board))) == 1:
            return True
        if Player.moves/2 == 50:
            if input("Is it a tie (yes/no) : ") in ['yes','y','Yes']:
                return True

    def isCheckMate(self, board):
        if not list(self.possibleMoves(board)) and self.isCheck(board):
            return True

    def turn(self, board):
        whoTurn = "\n{}'s turn,".format(self.name)
        warning = "Your King is in check "
        if self.isCheck(board):
            whoTurn = whoTurn + warning
        return whoTurn

    def getMove(self, board):
        print ("\n")
        while True:
            move=input("\nMake a move : ")
            if move == 'exit':
                break
            else:
                start, target = self.getPos(move)
                if (start, target) in self.possibleMoves(board):
                    return start, target
                else:
                    raise IndexError

    def makeCheck(self, start, target, board):
        self.doMove(board, start, target)
        retval = self.isCheck(board)

        self.unmove(board, start, target)
        return retval

    def isCheck(self, board):
        kingPos = self.kingPos(board)
        for opp in self.opponent.getPieces(board):
            if self.opponent.canMove(board, opp, kingPos):
                return True

    def doMove(self, board, start, target):
        self.oldPiece = None
        if target in board:
            self.oldPiece = board[target]
        board[target] = board[start]
        board[target].pos = target
        del board[start]
        board[target].noMoves += 1
        if board[target].pieceName is 'p' and not self.oldPiece:
            if abs(target[0]-start[0]) == 2:
                board[target].turn_moved_twosquares = self.playedturns
            elif abs(target[1]-start[1]) == abs(target[0]-start[0]) == 1:
                if self.color is 'white':
                    cappedPiece = (target[0]-1, target[1])
                else:
                    cappedPiece = (target[0]+1, target[1])
                self.savedpawn = board[cappedPiece]
                del board[cappedPiece]

    def unmove(self, board, start, target):
        board[start] = board[target]
        board[start].pos = start
        if self.oldPiece:
            board[target] = self.oldPiece
        else:
            del board[target]
        board[start].noMoves -= 1
        if board[start].pieceName is 'p' and not self.oldPiece:
            if abs(target[0]-start[0]) == 2:
                del board[start].turn_moved_twosquares
            elif abs(target[1]-start[1]) == abs(target[0]-start[0]) == 1:
                if self.color is 'white':
                    cappedPiece = (target[0]-1, target[1])
                else:
                    cappedPiece = (target[0]+1, target[1])
                board[cappedPiece] = self.savedpawn

    def canPromote(self, board, target):
        pro = 'empty'
        while pro.lower() not in ['kn','q']:
            pro = \
            input("You may promote your pawn:\n[Kn]ight [Q]ueen : ")
        board[target].promote(pro)

    def isPathClear(self, start, target, board):
        col, row = start[1], start[0]
        colNext, rowNext = target[1], target[0]
        if abs(row - rowNext) <= 1 and abs(col - colNext) <= 1:
            return True
        else:
            if rowNext > row and colNext == col:
                tmpstart = (row+1,col)
            elif rowNext < row and colNext == col:
                tmpstart = (row-1,col)
            elif rowNext == row and colNext > col:
                tmpstart = (row,col+1)
            elif rowNext == row and colNext < col:
                tmpstart = (row,col-1)
            elif rowNext > row and colNext > col:
                tmpstart = (row+1,col+1)
            elif rowNext > row and colNext < col:
                tmpstart = (row+1,col-1)
            elif rowNext < row and colNext > col:
                tmpstart = (row-1,col+1)
            elif rowNext < row and colNext < col:
                tmpstart = (row-1,col-1)
            if tmpstart in board:
                return False
            else:
                return self.isPathClear(tmpstart, target, board)

    def canMove(self, board, start, target):
        myPiece = board[start].pieceName.upper()
        if myPiece == 'R' and not self.isRook(start, target):
            return False
        elif myPiece == 'KN' and not self.isKnight(start, target):
            return False
        elif myPiece == 'P' and not self.isPawn(start, target, board):
            return False
        elif myPiece == 'B' and not self.isBishop(start, target):
            return False
        elif myPiece == 'Q' and not self.isQueen(start, target):
            return False
        elif myPiece == 'K' and not self.isKing(start, target):
            return False
        if myPiece in 'RPBQK':
            if not self.isPathClear(start, target, board):
                return False
        return True

    def isRook(self, start, target):
        if start[0] == target[0] or start[1] == target[1]:
            return True

    def isKnight(self, start, target):
        if abs(target[0]-start[0]) == 2 and abs(target[1]-start[1]) == 1:
            return True
        elif abs(target[0]-start[0]) == 1 and abs(target[1]-start[1]) == 2:
            return True

    def isPawn(self, start, target, board):
        if 'white' in self.color and target[0] < start[0]:
            return False
        elif 'black' in self.color and target[0] > start[0]:
            return False
        if start[0] == target[0]:
            return False
        if target in board:
            if abs(target[1]-start[1]) == abs(target[0]-start[0]) == 1:
                return True
        else:
            if start[1] == target[1]:
                if abs(target[0]-start[0]) == 1:
                    return True
                if board[start].noMoves is 0:
                    if abs(target[0]-start[0]) == 2:
                        return True
            if start[0] == self.capRow:
                if abs(target[0]-start[0]) == 1:
                    if abs(target[1]-start[1]) == 1:
                        if target[1]-start[1] == -1:
                            cappedPiece = (start[0], start[1]-1)
                        elif target[1]-start[1] == 1:
                            cappedPiece = (start[0], start[1]+1)
                        if cappedPiece in board and \
                        board[cappedPiece].color is not self.color and \
                        board[cappedPiece].pieceName is 'p'and \
                        board[cappedPiece].noMoves == 1 and \
                        board[cappedPiece].turn_moved_twosquares == \
                        self.playedturns-1:
                            return True

    def isBishop(self, start, target):
        if abs(target[1]-start[1]) == abs(target[0]-start[0]):
            return True

    def isQueen(self, start, target):
        if self.isRook(start, target) or self.isBishop(start, target):
            return True

    def isKing(self, start, target):
        if abs(target[0]-start[0]) <= 1 and abs(target[1]-start[1]) <= 1:
            return True