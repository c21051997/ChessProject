"""
This is responsible for:
	- storing all the information about the current game state.
	- determining the valid moves 
	- will keep a move log (for doing undo  and look back into current game) 
"""
import random

class GameState:
    def __init__(self):
        # board is a 8*8 2D list
        # each element is a 2 character long string consisting of
        # - lower case (b/w) as color
        # - upper case (R,N,B,A,C,Q,K or P) as piece name
        # in case the cell is empty then we store '--'
        whitePosition, blackPosition, kingPosition, queenRookPosition, kingRookPosition = self.startingPosition()
        self.board = [blackPosition,
					  ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
					  ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
					  ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
					  ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
					  ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
					  ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
					  whitePosition]
        """
        self.board = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                      ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                      ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]"""
        """
        self.board = [['bR', 'bN', 'bA', 'bB', 'bQ', 'bK', 'bB', 'bC', 'bN', 'bR'],
                      ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
                      ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
                      ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                      ['wR', 'wN', 'wA', 'wB', 'wQ', 'wK', 'wB', 'wC', 'wN', 'wR']]
        """

        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves, 
                              'A': self.getArchbishopMoves, 'C': self.getChancellorMoves}
        self.whiteToMove = True
        self.moveLog = []
        # Keeping track of kings to make valid move calculation and castling easier.
        self.whiteKingLocation = (7, kingPosition)
        self.blackKingLocation = (0, kingPosition)

        self.kingPosition = kingPosition
        self.queenRookPosition = queenRookPosition
        self.kingRookPosition = kingRookPosition

        # keep track of checkmate and stalemate
        self.checkMate = False
        self.staleMate = False

        self.enPassantPossible = ()

        # castling
        self.currentCastlingRights = CastleRights(True, True, True, True)
        # self.castleRightsLog =  [self.currentCastlingRights] # this will pose a problem as we are not copying the
        # self.currentCastlingRights object we are just storing another reference to it.
        self.castleRightsLog = [
            CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.wqs,  # correct way
                         self.currentCastlingRights.bks, self.currentCastlingRights.bqs)]

    '''
	A function to move pieces on the board and record them. (Won't work for castling, pawn-promotion and en-passant)
	'''
    def startingPosition(self):
                
        columns = list(range(10))

        #Random king postion, not on either edge as rooks must be either side
        kingPosition = random.randrange(1,9) 
        #kingPosition = 8
        columns.remove(kingPosition)
        #Random rook position either side of the king
        queenRookPosition = random.randrange(0, kingPosition)
        #queenRookPosition = 0
        kingRookPosition = random.randrange(kingPosition + 1, 10)
        #kingRookPosition = 2
        columns.remove(queenRookPosition)
        columns.remove(kingRookPosition)

        whiteSquare = False
        blackSquare = False
        bishopOnePosition = random.choice(columns)
        columns.remove(bishopOnePosition)
        
        if bishopOnePosition % 2 == 0:
            whiteSquare = True
        while not(blackSquare):
            bishopTwoPosition = random.choice(columns)
            if bishopTwoPosition % 2 != 0 and whiteSquare or bishopTwoPosition % 2 == 0 and not(whiteSquare):
                blackSquare = True
        columns.remove(bishopTwoPosition)

        #Knights, Chancellor, Archbishop, Queen left
        knightOnePosition, knightTwoPosition, chancellorPosition, archbishopPosition, queenPosition = random.sample(columns, 5)

        #print(knightOnePosition, knightTwoPosition, chancellorPosition, archbishopPosition, queenPosition, bishopTwoPosition, bishopOnePosition, rightRookPosition, leftRookPosition, kingPosition)

        whitePieces = {
            knightOnePosition:'wN',
            knightTwoPosition:'wN',
            bishopOnePosition: 'wB',
            bishopTwoPosition: 'wB',
            queenRookPosition: 'wR',
            kingRookPosition: 'wR',
            archbishopPosition: 'wA',
            chancellorPosition: 'wC',
            queenPosition: 'wQ',
            kingPosition:'wK'
        }

        blackPieces = {
            knightOnePosition:'bN',
            knightTwoPosition:'bN',
            bishopOnePosition: 'bB',
            bishopTwoPosition: 'bB',
            queenRookPosition: 'bR',
            kingRookPosition: 'bR',
            archbishopPosition: 'bA',
            chancellorPosition: 'bC',
            queenPosition: 'bQ',
            kingPosition:'bK'
        }

        whitePosition = [whitePieces.get(i) for i in range(10)]
        blackPosition = [blackPieces.get(i) for i in range(10)]
        return whitePosition, blackPosition, kingPosition, queenRookPosition, kingRookPosition

    def makeMove(self, move):

        if not move.isCastleMove:
            self.board[move.startRow][move.startCol] = '--'  # empty the start cell
            self.board[move.endRow][move.endCol] = move.pieceMoved  # keep the piece moved on the end cell
            self.moveLog.append(move)  # record the move
            #print(self.board[move.startRow][move.startCol])
            #print(self.board[move.endRow][move.endCol])
            # UPDATE KING'S POSITION
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        # Pawn Promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[
                                                    0] + 'Q'  # hardcoding Q for now. will include options later.

        # En-Passant
        if move.isEnPassantMove:
            self.board[move.startRow][move.endCol] = '--'  # Capturing the Piece

        # Update enPassantPossible Variable
        if move.pieceMoved[1] == 'P' and abs(move.endRow - move.startRow) == 2:  # only on 2 sq. pawn advance
            self.enPassantPossible = ((move.startRow + move.endRow) // 2, move.endCol)
        else:
            self.enPassantPossible = ()

        '''
        CHANGE THIS
        '''
        # castle Move
        #if move.pieceMoved[1] == 'K' and
        #print(move.isCastleMove)
        if move.isCastleMove:
            #if move.endCol == self.queenRookPosition:  # Queen side castle
            if move.endCol < move.startCol:
                self.board[move.startRow][move.startCol] = '--'
                self.board[move.endRow][self.queenRookPosition] = '--'
                self.board[move.endRow][2] = move.pieceMoved 
                #self.board[move.endRow][move.endCol + 1] = move.pieceMoved[0] + 'R'
                self.board[move.endRow][3] = move.pieceMoved[0] + 'R'
            else:  # King side castle
                self.board[move.startRow][move.startCol] = '--'
                self.board[move.endRow][self.kingRookPosition] = '--'
                self.board[move.endRow][8] = move.pieceMoved 
                #self.board[move.endRow][move.endCol - 1] = move.pieceMoved[0] + 'R'
                self.board[move.endRow][7] = move.pieceMoved[0] + 'R'
            self.moveLog.append(move)
        # Update 7. Castling Rights
        self.updateCastlingRights(move)
        newCastleRights = CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.wqs,
                                    self.currentCastlingRights.bks, self.currentCastlingRights.bqs)
        self.castleRightsLog.append(newCastleRights)

        self.whiteToMove = not self.whiteToMove  # swap the turn

    '''
	Undo a move.
	'''

    def undoMove(self):
        if len(self.moveLog) == 0:
            print('No move done till now. Can\'t UNDO at the start of the game')
            return
        move = self.moveLog.pop()
        if not move.isCastleMove:
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
        self.whiteToMove = not self.whiteToMove

            # UPDATE KING'S POSITION
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.startRow, move.startCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.startRow, move.startCol)

        # Undo Enpassant Move
        if move.isEnPassantMove:
            self.board[move.endRow][move.endCol] = '--'
            self.board[move.startRow][move.endCol] = move.pieceCaptured
            self.enPassantPossible = (move.endRow, move.endCol)

        # UNDO a 2 sq pawn advance
        if move.pieceMoved[1] == 'P' and abs(move.endRow - move.startRow) == 2:
            self.enPassantPossible = ()
            
        # UNDO castling rights:
        self.castleRightsLog.pop()  # get rid of last 7. Castling right
        self.currentCastlingRights.wks = self.castleRightsLog[-1].wks  # update current castling right
        self.currentCastlingRights.wqs = self.castleRightsLog[-1].wqs  # update current castling right
        self.currentCastlingRights.bks = self.castleRightsLog[-1].bks  # update current castling right
        self.currentCastlingRights.bqs = self.castleRightsLog[-1].bqs  # update current castling right
        '''
        
        MAYBE CHANGE THIS

        '''
        # UNDO CASTLING MOVE:
        """if move.isCastleMove:
            if move.endCol < move.startCol:  # Queen Side Castle
                self.board[move.endRow][move.endCol + 1] = '--'
                self.board[move.endRow][0] = move.pieceMoved[0] + 'R'
            else:  # King side castle
                self.board[move.endRow][move.endCol - 1] = '--'
                self.board[move.endRow][7] = move.pieceMoved[0] + 'R'"""
        if move.isCastleMove:
            #if move.endCol == self.queenRookPosition:  # Queen side castle
            if move.endCol < move.startCol:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.endRow][3] = '--'
                self.board[move.startRow][self.kingPosition] = move.pieceMoved 
                #self.board[move.endRow][move.endCol + 1] = move.pieceMoved[0] + 'R'
                self.board[move.endRow][self.queenRookPosition] = move.pieceMoved[0] + 'R'
            else:  # King side castle
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.endRow][7] = '--'
                self.board[move.startRow][self.kingPosition] = move.pieceMoved 
                #self.board[move.endRow][move.endCol - 1] = move.pieceMoved[0] + 'R'
                self.board[move.endRow][self.kingRookPosition] = move.pieceMoved[0] + 'R'
        
    '''
	Updating 7. Castling Right given a Move -> -> when it's a Rook or a King Move
	'''

    def updateCastlingRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRights.wqs = False
            self.currentCastlingRights.wks = False

        elif move.pieceMoved == 'bK':
            self.currentCastlingRights.bqs = False
            self.currentCastlingRights.bks = False

        elif move.pieceMoved == 'wR':
            if move.startRow == 7 and move.startCol == self.queenRookPosition:
                self.currentCastlingRights.wqs = False
            if move.startRow == 7 and move.startCol == self.kingRookPosition:
                self.currentCastlingRights.wks = False

        elif move.pieceMoved == 'bR':
            if move.startRow == 0 and move.startCol == self.queenRookPosition:
                self.currentCastlingRights.bqs = False
            if move.startRow == 0 and move.startCol == self.kingRookPosition:
                self.currentCastlingRights.bks = False

    ''' 
	Get a list of all the valid moves -> the moves that user can actually make. => Considering CHECKS.
	'''

    def getValidMoves(self):
        tempEnPassant = self.enPassantPossible
        tempCastlingRights = self.currentCastlingRights
        # 1) Get a List of all possible Moves
        moves = self.getAllPossibleMoves()
        currentKingLocation = self.whiteKingLocation if self.whiteToMove else self.blackKingLocation
        #get 7. Castling Moves
        self.getCastlingMoves(currentKingLocation[0], currentKingLocation[1], moves)
        #print(self.getCastlingMoves(currentKingLocation[0], currentKingLocation[1], moves))
        # 2) Make a move from the list of possible moves
        for i in range(len(moves) - 1, -1,
                       -1):  # travering in opposite direction cause we have to remove some elements from the middle.
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove  # for generating opponent's move change turn
            # 3) Generate all of the opponents move after making the move in previous stel
            # 4) Check if any of the opponents move leads to check -> if so remove the move from our list
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        # 5) Return the final list of moves
        if len(moves) == 0:
            """if self.inCheck():
                print("CHECK MATE! " + ('white' if not self.whiteToMove else 'black') + " wins")

                self.checkMate = True
            else:
                print("DRAW DUE TO STALEMATE")
                self.staleMate = True"""
        else:
            self.checkMate = False
            self.staleMate = False
        self.enPassantPossible = tempEnPassant
        self.currentCastlingRights = tempCastlingRights
        return moves

    '''
	Checks if the current player is under check
	'''

    def inCheck(self):
        if self.whiteToMove:
            return self.isUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.isUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    '''
	Checks if sq (r,c) is under attack or not
	'''

    def isUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove  # switch to opponent's turn
        opponentsMove = self.getAllPossibleMoves()  # generate opponents move
        self.whiteToMove = not self.whiteToMove  # switch back turns
        for move in opponentsMove:
            if move.endRow == r and move.endCol == c:  # sq under attack
                return True
        return False

    '''
	Get a list of all possible moves -> Without considering CHECKS
	'''

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                piece = self.board[r][c][1]
                if not (self.whiteToMove ^ (turn == 'w')):
                    if piece != '-':
                        self.moveFunctions[piece](r, c, moves)  # call appropriate get piece move function
        return moves

    '''
	Get all possible moves for a pawn located at (r,c) and add the moves to the list.
	'''

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove and self.board[r][c][0] == 'w':  # WHITE PAWN MOVES
            if self.board[r - 1][c] == '--':  # 1 square pawn advance
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == '--':  # 2 square pawn advance
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == 'b':  # enemy piece to capture to the left
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                if self.enPassantPossible == (r - 1, c - 1):
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEnPassantMove=True))
            if c + 1 < len(self.board):
                if self.board[r - 1][c + 1][0] == 'b':  # enemy piece to capture to the right
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                if self.enPassantPossible == (r - 1, c + 1):
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEnPassantMove=True))

        if not self.whiteToMove and self.board[r][c][0] == 'b':  # BLACK PAWN MOVES
            if self.board[r + 1][c] == '--':  # 1 square pawn advance
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == '--':  # 2 square pawn advance
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':  # enemy pice to capture to the left
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                if self.enPassantPossible == (r + 1, c - 1):
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnPassantMove=True))
            if c + 1 < len(self.board):
                if self.board[r + 1][c + 1][0] == 'w':  # enemy pice to capture to the right
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                if self.enPassantPossible == (r + 1, c + 1):
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnPassantMove=True))

    '''
	Get all possible moves for a Rook located at (r,c) and add the moves to the list.
	'''

    def getRookMoves(self, r, c, moves):

        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))  # up down left right
        enemyColor = 'b' if self.whiteToMove else 'w'  # opponenet's color according to current turn
        for d in directions:
            for i in range(1, 10):
                endRow = r + (d[0] * i)
                endCol = c + (d[1] * i)
                if endRow >= 0 and endRow < len(self.board) and endCol >= 0 and endCol < len(self.board[endRow]):
                    if self.board[endRow][endCol] == '--':  # Empty Square
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif self.board[endRow][endCol][0] == enemyColor:  # capture opponent's piece
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break  # same color piece
                else:
                    break  # off board

    '''
	Get all possible moves for a Knight located at (r,c) and add the moves to the list.
	'''

    def getKnightMoves(self, r, c, moves):
        directions = ((-1, -2), (-2, -1), (1, -2), (2, -1), (1, 2), (2, 1), (-1, 2), (-2, 1))
        allyColor = 'w' if self.whiteToMove else 'b'  # opponenet's color according to current turn
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if endRow >= 0 and endRow < len(self.board) and endCol >= 0 and endCol < len(self.board[endRow]):
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    '''
	Get all possible moves for a Bishop located at (r,c) and add the moves to the list.
	'''

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # (top left) (top right) (bottom left) (bottom right)
        enemyColor = 'b' if self.whiteToMove else 'w'  # opponenet's color according to current turn
        for d in directions:
            for i in range(1, 10):
                endRow = r + (d[0] * i)
                endCol = c + (d[1] * i)
                if endRow >= 0 and endRow < len(self.board) and endCol >= 0 and endCol < len(self.board[endRow]):
                    if self.board[endRow][endCol] == '--':  # Empty Square
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif self.board[endRow][endCol][0] == enemyColor:  # capture opponent's piece
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break  # same color piece
                else:
                    break  # off board

    '''
	Get all possible moves for a Queen located at (r,c) and add the moves to the list.
	'''

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    '''
	Get all possible moves for a King located at (r,c) and add the moves to the list.
	'''

    def getKingMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = 'w' if self.whiteToMove else 'b'  # ally color according to current turn
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if endRow >= 0 and endRow < len(self.board) and endCol >= 0 and endCol < len(self.board[endRow]):
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
    
    def getArchbishopMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getKnightMoves(r, c, moves)

    def getChancellorMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getKnightMoves(r, c, moves)

    '''
	Gets the list of all of the king's castling move -> for the king at(r,c);
	'''

    def getCastlingMoves(self, r, c, moves):
        if self.inCheck():
            return  # can't castle when king is under attack

        if (self.whiteToMove and self.currentCastlingRights.wks) or \
                (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingSideCastleMoves(r, c, moves)

        if (self.whiteToMove and self.currentCastlingRights.wqs) or \
                (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueenSideCastleMoves(r, c, moves)

    '''

    CHANGE THIS FOR CORRECT CASTLING
    > GET POSITION OF KING / ROOK
    > SEE IF NO PIECES ARE BETWEEN
    > SEE IF PIECES HAVENT BEEN MOVES

    '''

    def getKingSideCastleMoves(self, r, c, moves):
        '''
        for distance between king and rook
            if self.board[r][c + i] == '--' and not self.isUnderAttack(r, c + i)
                permission = true
        if [r][c] != Where the king is castling to (normal chess positions)
            
        if permission == true

        '''
        castlePermission = False
        difference = abs(c - 8)

        for i in range(1, difference + 1):

            if ((self.board[r][c + i] == '--') or (self.board[r][c + i][1] == 'R')) and not self.isUnderAttack(r, c + i):
                castlePermission = True
            else:
                castlePermission = False
                break
        if c == 7:
            if (self.board[r][8] == '--') or (self.board[r][8][1] == 'R'):
                # If the king is on the Rook square after castling (Column 8) then let the king castle if .. 
                # the square is empty or there is a rook on there
                castlePermission == True
        if c == 8:
            if (self.board[r][7] == '--') and (self.board[r][9][1] == 'R'):
                # If the King is on the Castle Square (Column 9) then allow rook to move to column 7
                # This imitates castling movement
                moves.append(Move((r, 9), (r, 7), self.board))
            
        if castlePermission == True:
            moves.append(Move((r, c), (r, 8), self.board, isCastleMove=True))
        """
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--' and self.board[r][c + 3] == '--':
            if not self.isUnderAttack(r, c + 1) and not self.isUnderAttack(r, c + 2) and not self.isUnderAttack(r, c + 3):
                moves.append(Move((r, c), (r, c + 3), self.board, isCastleMove=True))
        """
    def getQueenSideCastleMoves(self, r, c, moves):
        """
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--' and self.board[r][c - 4] == '--':
            if not self.isUnderAttack(r, c - 1) and not self.isUnderAttack(r, c - 2) and not self.isUnderAttack(r, c - 3):
                moves.append(Move((r, c), (r, c - 3), self.board, isCastleMove=True))
        """
        """
        castlePermission = False
        if c > 2:
            difference = abs(c - 2)
            for i in range(1, difference + 1):
                if ((self.board[r][c - i] == '--') or (self.board[r][c - i][1] == 'R')) and not self.isUnderAttack(r, c - i):
                    castlePermission = True
                elif difference == 0 and self.board[r][c + 1] == '--':
                    castlePermission = True
                else:
                    castlePermission = False
                    break
        elif c == 3:
            if (self.board[r][2] == '--') or (self.board[r][2][1] == 'R'):
                castlePermission = True
        #else: 
            #if (self.board[r][c + 1] == '--' and not self.isUnderAttack(r, c + 1)):
               #castlePermission = True
        
        if castlePermission and self.board[r][0][1] == 'R':
            if self.board[r][1] != '__':
                castlePermission = False

        if castlePermission == True:
            moves.append(Move((r, c), (r, 2), self.board, isCastleMove=True))
        """
        castlePermission = False

        if c > 2:
            difference = abs(c - 2)
            for i in range(1, difference + 1):
                if (self.board[r][c - i] == '--' or self.board[r][c - i][1] == 'R') and not self.isUnderAttack(r, c - i):
                    castlePermission = True
                else:
                    castlePermission = False
                    break

        if c == 3:
            if self.board[r][2] == '--' or self.board[r][2][1] == 'R':
                castlePermission = True

        if c == 2:
            if self.board[r][3] == '--':
                if self.board[r][1][1] == 'R': 
                    moves.append(Move((r, 1), (r, 3), self.board))
                elif self.board[r][1] == '--':
                    moves.append(Move((r, 0), (r, 3), self.board))

        if castlePermission and self.board[r][0][1] == 'R':
            if self.board[r][1] != '--':
                castlePermission = False

        if castlePermission:
            moves.append(Move((r, c), (r, 2), self.board, isCastleMove=True))
    """
    > Have a clicks function
    > Check if first click is king, second rook
    > Then check for the castle moves
    """

class CastleRights:

    def __init__(self, wks, wqs, bks, bqs):
        self.wks = wks
        self.wqs = wqs
        self.bks = bks
        self.bqs = bqs

    '''
    Overloading the __str__ function to print the 7. Castling Rights Properly
    '''
    def __str__(self):
        return ("7. Castling Rights(wk, wq, bk, bq) : " + str(self.wks) + " " + str(self.wqs) + " " + str(
            self.bks) + " " + str(self.bqs))

class Move:
    # maps keys to values
    # For converting (row, col) to Chess Notations => (0,0) -> a8
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7,
                   "i": 8, "j":9}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnPassantMove=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]  # can't be '--'
        self.pieceCaptured = board[self.endRow][self.endCol]  # can be '--' -> no piece was captured
        # Pawn Promotion
        self.isPawnPromotion = (self.pieceMoved == 'wP' and self.endRow == 0) or (
                self.pieceMoved == 'bP' and self.endRow == 7)

        # En Passant
        self.isEnPassantMove = isEnPassantMove
        if self.isEnPassantMove:
            self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'

        # CastleMove
        self.isCastleMove = isCastleMove

        self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def getChessNotation(self):
        return self.getFileRank(self.startRow, self.startCol) + self.getFileRank(self.endRow, self.endCol)

    def getFileRank(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    '''
	overriding equal to method
	'''

    def __eq__(self, other):
        return isinstance(other, Move) and self.moveId == other.moveId

    