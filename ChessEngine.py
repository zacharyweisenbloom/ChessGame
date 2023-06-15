from shutil import move


class GameState():
    def __init__(self):
        # board is an 8x8 2 dimensional list. The first charecter represents the color the second represents the pieces. 

        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["0",  "0",  "0",  "0",  "0",  "0",  "0",  "0"],
            ["0",  "0",  "0",  "0",  "0",  "0",  "0",  "0"],
            ["0",  "0",  "0",  "0",  "0",  "0",  "0",  "0"],
            ["0",  "0",  "0",  "0",  "0",  "0",  "0",  "0"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K' : self.getKingMoves}
        
        self.white_to_move = True
        self.white_king_location = (7,4)
        self.black_king_location = (0,4)

        self.move_log = []

    """this will not work for castling, pawn promotion and en-passant."""
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "0"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        if move.pieceMoved == "wK":
            self.white_king_location = (move.endRow,move.endCol)
        if move.pieceMoved == "bK":
            self.black_king_location = (move.endRow,move.endCol)

            print("king move")
    """Undo the last move made."""

    def undoMove(self):
        if len(self.move_log) != 0:
            move  = self.move_log.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.white_to_move = not self.white_to_move
            if move.pieceMoved == "wK":
                self.white_king_location = (move.startRow,move.startCol)
            if move.pieceMoved == "bK":
                self.black_king_location = (move.startRow,move.startCol)
    
    """All moves considering Checks"""
    def getValidMoves(self):
        moves = self.getAllPossibleMoves()

        return moves

    """All moves without considering checks."""
    def getAllPossibleMoves(self):
        moves= []
        print("here")
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        return moves

    def getPawnMoves(self, r,c,moves):
        print("Got pawn moves.")
        if self.white_to_move:
            if self.board[r-1][c] == '0':
                moves.append(Move((r,c), (r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == '0':
                    moves.append(Move((r,c), (r-2,c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r,c), (r-1,c-1), self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c), (r-1, c+1), self.board))
        else:
            if self.board[r+1][c] == '0':
                moves.append(Move((r,c),(r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == '0':
                    moves.append(Move((r,c), (r+2,c), self.board))
            if c - 1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c), (r+1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1] == 'w':
                    moves.append(Move((r,c), (r+1, c-1), self.board))
     
    def getRookMoves(self, r,c,moves):
        directions = ((-1,0), (0,-1), (1,0), (0,1))
        enemyColor = "b" if self.white_to_move else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "0":
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
        """
        up = True
        left = True
        down = True
        right = True

        
        if self.white_to_move:
            for i in range(1,8):
                if (c - i >= 0) and down==True:
                    if self.board[r][c-i] == '0':
                        moves.append(Move(r,c), (r,c-i), self.board)
                    else:
                        if self.board[r][c-i] == 'b':
                            moves.append(Move(r,c), (r,c-i), self.board)
                        down = False
            for i in range(1,8):
                if (c + i <= 7) and up==True:
                    if self.board[r][c+i] == '0':
                        moves.append(Move(r,c), (r,c+i), self.board)
                    else:
                        if self.board[r][c+i] == 'b':
                            moves.append(Move(r,c), (r,c+i), self.board)
                        up = False
                        

        return moves
        """
        

    def getKnightMoves(self,r,c,moves):
        knightMoves = ((-2,-1), (-2,1), (-1, -2), (-1,2), (1,-2,), (1,2), (2,-1), (2,1))
        print("knight")
        allyColor = 'w' if self.white_to_move else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if (0 <= endRow <= 7) and (0 <= endCol <= 7):
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c), (endRow, endCol), self.board))


    def getBishopMoves(self,r,c,moves):
        bishopMoves = ((1,1),(1,-1),(-1,-1),(-1,1))
        allyColor = 'w' if self.white_to_move else "b"
        for m in bishopMoves:
            for i in range(1,8):
                endRow = r + m[0]*i
                endCol = c + m[1]*i
                if (0 <= endRow <= 7) and (0 <= endCol <= 7):
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
            
                
    def getQueenMoves(self,r,c,moves):
        self.getBishopMoves(r,c,moves)
        self.getRookMoves(r,c,moves)


    def getKingMoves(self, r,c,moves):
        directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (1,1), (-1,1),(1,-1))
        enemyColor = "b" if self.white_to_move else 'w'
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "0":
                    moves.append(Move((r,c), (endRow, endCol), self.board))
                elif endPiece[0] == enemyColor:
                    moves.append(Move((r,c), (endRow, endCol), self.board))


class Move():
    """
    ranksToRows = {"1": 7,  "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e" : 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items}
    """
    def __init__(self, startsq, endsq, board) -> None:

        self.ranksToRows = {"1": 7,  "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
        self.rowsToRanks = {v: k for k, v in self.ranksToRows.items()}
        self.filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e" : 4, "f": 5, "g": 6, "h": 7}
        self.colsToFiles = {v: k for k, v in self.filesToCols.items()}

        self.startRow = startsq[0]
        self.startCol = startsq[1]
        self.endRow = endsq[0]
        self.endCol = endsq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.MoveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
    """Overiding the equals method."""

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.MoveID == other.MoveID
        return False
    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


 
