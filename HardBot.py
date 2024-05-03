import random
from timeit import default_timer as timer


DEPTH = 3
PIECE_VALUES = {'P': 100, 'N': 320, 'B': 330, 'R':500, 'A': 700, 'C': 800, 'Q': 900, 'K': 10000}
STALEMATE = -10000
CHECKMATE = 10000

PAWN_TABLE = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [50, 50, 50, 50, 50, 50, 50, 50, 50, 50],
              [10, 10, 20, 20, 30, 30, 20, 20, 10, 10],
              [5, 5, 10, 15, 25, 25, 15, 10, 5, 5],
              [0, 0, 0, 10, 20, 20, 10, 0, 0, 0],
              [5, -5, -10, 0, 0, 0, 0, -10, -5, 5],
              [5, 10, 10, -10, -20, -20, -10, 10, 10, 5],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

KNIGHT_TABLE = [[-50, -40, -30, -30, -30, -30, -30, -30, -40, -50],
                [-40, -20, -10, 0, 0, 0, 0, -10, -20, -40],
                [-30, 0, 5, 10, 15, 15, 10, 5, 0, -30],
                [-30, 5, 10, 15, 20, 20, 15, 10, 5, -30],
                [-30, 0, 10, 15, 20, 20, 15, 10, 0, -30],
                [-30, 5, 5, 10, 15, 15, 10, 5, 5, -30],
                [-40, -20, -10, 0, 5, 5, 0, -10, -20, -40],
                [-50, -40, -30, -30, -30, -30, -30, -30, -40, -50]]

BISHOP_TABLE = [[-20, -10, -10, -10, -10, -10, -10, -10, -10, -20],
                [-10, 0, 0, 0, 0, 0, 0, 0, 0, -10],
                [-10, 0, 5, 5, 10, 10, 5, 5, 0, -10],
                [-10, 5, 5, 5, 10, 10, 5, 5, 5, -10],
                [-10, 0, 10, 10, 10, 10, 10, 10, 0, -10],
                [-10, 10, 10, 10, 10, 10, 10, 10, 10, -10],
                [-20, -10, -10, -10, -10, -10, -10, -10, -10, -20]]

ROOK_TABLE = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [5, 10, 10, 10, 10, 10, 10, 10, 10, 5],
              [-5, 0, 0, 0, 0, 0, 0, 0, 0, -5],
              [-5, 0, 0, 0, 0, 0, 0, 0, 0, -5],
              [-5, 0, 0, 0, 0, 0, 0, 0, 0, -5],
              [-5, 0, 0, 0, 0, 0, 0, 0, 0, -5],
              [-5, 0, 0, 0, 0, 0, 0, 0, 0, -5],
              [0, 0, 0, 0, 5, 5, 0, 0, 0, 0]]

QUEEN_TABLE = [[-20, -10, -10, -10, -5, -5, -10, -10, -10, -20],
               [-10, 0, 0, 0, 0, 0, 0, 0, 0, -10],
               [-10, 0, 0, 5, 5, 5, 5, 0, 0, -10],
               [-5, 0, 0, 5, 5, 5, 5, 0, 0, -5],
               [0, 0, 5, 5, 5, 5, 5, 5, 0, 0],
               [-10, 5, 5, 5, 5, 5, 5, 5, 0, -10],
               [-10, 0, 5, 5, 0, 0, 0, 0, 0, -10],
               [-20, -10, -10, -10, -5, -5, -10, -10, -10, -20]]

KING_TABLE = [[-30, -40, -40, -40, -50, -50, -40, -40, -40, -30],
              [-30, -40, -40, -40, -50, -50, -40, -40, -40, -30],
              [-30, -40, -40, -40, -50, -50, -40, -40, -40, -30],
              [-30, -40, -40, -40, -50, -50, -40, -40, -40, -30],
              [-20, -30, -30, -30, -40, -40, -30, -30, -30, -20],
              [-10, -20, -20, -20, -20, -20, -20, -20, -20, -10],
              [20, 20, 10, 0, 0, 0, 0, 10, 20, 20],
              [20, 30, 20, 10, 0, 0, 10, 20, 30, 20]]

ARCHBISHOP_TABLE = [[-35, -25, -20, -20, -20, -20, -20, -20, -25, -35],
                    [-25, -10, -5, 0, 0, 0, 0, -5, -10, -25],
                    [-20, 0, 5, 7.5, 12.5, 12.5, 7.5, 5, 0, -20],
                    [-20, 5, 7.5, 10, 15, 15, 10, 7.5, 5, -20],
                    [-20, 0, 10, 10, 15, 15, 10, 10, 0, -20],
                    [-20, 7.5, 7.5, 10, 12.5, 12.5, 10, 7.5, 7.5, -20],
                    [-25, -7.5, -10, 0, 2.5, 2.5, 0, -10, -7.5, -25],
                    [-35, -25, -20, -20, -20, -20, -20, -20, -25, -35]]

CHANCELLOR_TABLE = [[-25, -20, -15, -15, -15, -15, -15, -15, -20, -25],
                    [-17.5, -5, 0, 5, 5, 5, 5, 0, -5, -17.5],
                    [-17.5, 0, 2.5, 5, 7.5, 7.5, 5, 2.5, 0, -17.5],
                    [-17.5, 2.5, 5, 7.5, 10, 10, 7.5, 5, 2.5, -17.5],
                    [-17.5, 0, 5, 7.5, 10, 10, 7.5, 5, 0, -17.5],
                    [-17.5, 2.5, 2.5, 5, 7.5, 7.5, 5, 2.5, 2.5, -17.5],
                    [-22.5, -10, -5, 0, 2.5, 2,5, 0, -5, -10, -22.5],
                    [-25, -20, -15, -15, -15, -15, -15, -15, -20, -25]]
                    
BLACK_PAWN_TABLE = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [5, 10, 10, -10, -20, -20, -10, 10, 10, 5],
                    [5, -5, -10, 0, 0, 0, 0, -10, -5, 5],
                    [0, 0, 0, 10, 20, 20, 10, 0, 0, 0],
                    [5, 5, 10, 15, 25, 25, 15, 10, 5, 5],
                    [10, 10, 20, 20, 30, 30, 20, 20, 10, 10],
                    [50, 50, 50, 50, 50, 50, 50, 50, 50, 50],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

BLACK_KNIGHT_TABLE = [[-50, -40, -30, -30, -30, -30, -30, -30, -40, -50],
                      [-40, -20, -10, 0, 5, 5, 0, -10, -20, -40],
                      [-30, 5, 5, 10, 15, 15, 10, 5, 5, -30],
                      [-30, 0, 10, 15, 20, 20, 15, 10, 0, -30],
                      [-30, 5, 10, 15, 20, 20, 15, 10, 5, -30],
                      [-30, 0, 5, 10, 15, 15, 10, 5, 0, -30],
                      [-40, -20, -10, 0, 0, 0, 0, -10, -20, -40],
                      [-50, -40, -30, -30, -30, -30, -30, -30, -40, -50]]

BLACK_BISHOP_TABLE = [[-20, -10, -10, -10, -10, -10, -10, -10, -10, -20],
                [-10, 10, 10, 10, 10, 10, 10, 10, 10, -10],
                [-10, 0, 10, 10, 10, 10, 10, 10, 0, -10],
                [-10, 5, 5, 5, 10, 10, 5, 5, 5, -10],
                [-10, 0, 5, 5, 10, 10, 5, 5, 0, -10],
                [-10, 0, 0, 0, 0, 0, 0, 0, 0, -10],
                [-20, -10, -10, -10, -10, -10, -10, -10, -10, -20]]

BLACK_ROOK_TABLE = [[0, 0, 0, 0, 5, 5, 0, 0, 0, 0],
                    [-5, 0, 0, 0, 0, 0, 0, 0, 0, -5],
                    [-5, 0, 0, 0, 0, 0, 0, 0, 0, -5],
                    [-5, 0, 0, 0, 0, 0, 0, 0, 0, -5],
                    [-5, 0, 0, 0, 0, 0, 0, 0, 0, -5],
                    [-5, 0, 0, 0, 0, 0, 0, 0, 0, -5],
                    [5, 10, 10, 10, 10, 10, 10, 10, 10, 5]]

BLACK_QUEEN_TABLE = [[-20, -10, -10, -10, -5, -5, -10, -10, -10, -20],
                     [-10, 0, 0, 0, 0, 0, 5, 5, 0, -10],
                     [-10, 0, 5, 5, 5, 5, 5, 5, 5, -10],
                     [0, 0, 5, 5, 5, 5, 5, 5, 0, 0],
                     [-5, 0, 0, 5, 5, 5, 5, 0, 0, -5],
                     [-10, 0, 0, 5, 5, 5, 5, 0, 0, -10],
                     [-10, 0, 0, 0, 0, 0, 0, 0, 0, -10],
                     [-20, -10, -10, -10, -5, -5, -10, -10, -10, -20]]

BLACK_KING_TABLE = [[20, 30, 20, 10, 0, 0, 10, 20, 30, 20],
                    [20, 20, 10, 0, 0, 0, 0, 10, 20, 20],
                    [-10, -20, -20, -20, -20, -20, -20, -20, -20, -10],
                    [-20, -30, -30, -30, -40, -40, -30, -30, -30, -20],
                    [-30, -40, -40, -40, -50, -50, -40, -40, -40, -30],
                    [-30, -40, -40, -40, -50, -50, -40, -40, -40, -30],
                    [-30, -40, -40, -40, -50, -50, -40, -40, -40, -30],
                    [-30, -40, -40, -40, -50, -50, -40, -40, -40, -30]]

BLACK_ARCHBISHOP_TABLE = [[-35, -25, -20, -20, -20, -20, -20, -20, -25, -35],
                    [-25, -7.5, -10, 0, 2.5, 2.5, 0, -10, -7.5, -25],
                    [-20, 7.5, 7.5, 10, 12.5, 12.5, 10, 7.5, 7.5, -20],
                    [-20, 0, 10, 10, 15, 15, 10, 10, 0, -20],
                    [-20, 5, 7.5, 10, 15, 15, 10, 7.5, 5, -20],
                    [-20, 0, 5, 7.5, 12.5, 12.5, 7.5, 5, 0, -20],
                    [-25, -10, -5, 0, 0, 0, 0, -5, -10, -25],
                    [-35, -25, -20, -20, -20, -20, -20, -20, -25, -35]]

BLACK_CHANCELLOR_TABLE = [[-25, -20, -15, -15, -15, -15, -15, -15, -20, -25],
                          [-22.5, -10, -5, 0, 2.5, 2,5, 0, -5, -10, -22.5],
                          [-17.5, 2.5, 2.5, 5, 7.5, 7.5, 5, 2.5, 2.5, -17.5],
                          [-17.5, 0, 5, 7.5, 10, 10, 7.5, 5, 0, -17.5],
                          [-17.5, 2.5, 5, 7.5, 10, 10, 7.5, 5, 2.5, -17.5],
                          [-17.5, 0, 2.5, 5, 7.5, 7.5, 5, 2.5, 0, -17.5],
                          [-17.5, -5, 0, 5, 5, 5, 5, 0, -5, -17.5],
                          [-25, -20, -15, -15, -15, -15, -15, -15, -20, -25]]

PIECE_TABLE_VALUES = {"P": PAWN_TABLE, "N": KNIGHT_TABLE, 
                      "B": BISHOP_TABLE, "R": ROOK_TABLE, 
                      "Q": QUEEN_TABLE, "A": ARCHBISHOP_TABLE,
                      "C": CHANCELLOR_TABLE, "K": KING_TABLE }

BLACK_PIECE_TABLE_VALUES = {"P": BLACK_PAWN_TABLE, "N": BLACK_KNIGHT_TABLE, 
                            "B": BLACK_BISHOP_TABLE, "R": BLACK_ROOK_TABLE, 
                            "Q": BLACK_QUEEN_TABLE, "A": BLACK_ARCHBISHOP_TABLE,
                            "C": BLACK_CHANCELLOR_TABLE, "K": BLACK_KING_TABLE }

def orderMoves(validMoves):
    #Checks
    #Captures
    captures = []
    normalMoves = []
    moveOrder = []
    for move in validMoves:
        """if move.inCheck():
            moveOrder.append(move)"""
        if move.pieceCaptured != "--":
            moveOrder.append(move)
        else:
            normalMoves.append(move)
    #moveOrder.extend(captures)
    moveOrder.extend(normalMoves)
    return moveOrder


def boardScore(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE   # BLACK WINS
        else:
            return CHECKMATE
    if gs.staleMate:
        if gs.whiteToMove:
            return CHECKMATE   # BLACK WINS
        else:
            return -CHECKMATE
        
        
    score = 0
    for rowNum, row in enumerate(gs.board):
        for columnNum, square in enumerate(row):

            if square != "--":
                if gs.whiteToMove:
                    pieceTableValue = PIECE_TABLE_VALUES[square[1]][rowNum -1][columnNum - 1]
                else:
                    pieceTableValue = BLACK_PIECE_TABLE_VALUES[square[1]][rowNum -1][columnNum - 1]

            if square[0] == 'w':
                score += PIECE_VALUES[square[1]] + pieceTableValue
            elif square[0] == 'b':
                score -= PIECE_VALUES[square[1]] + pieceTableValue
    return score

def quiesce(gs, alpha, beta):
    staticPosition = boardScore(gs)

    if staticPosition >= beta:
        return beta
    
    alpha = max(alpha, staticPosition)

    for move in gs.getValidMoves():
        if move.isCapture:
            gs.makeMove(move)
            score = -quiesce(gs, -beta, -alpha)
            gs.undoMove()

            if score >= beta:
                return beta
            alpha = max(alpha, score)

    return alpha


def negaMax(gs, depth, alpha, beta, turnMultiplier):
    if depth == 0:
        return None, turnMultiplier * boardScore(gs)
        
    moveOrder = orderMoves(gs.getValidMoves())
    if (len(gs.getValidMoves()) != len(moveOrder)):
        print("hey")
    bestMove = None
    global scores
    maxScore = -10000
    for move in moveOrder:
        gs.makeMove(move)
        score = -negaMax(gs, depth - 1, -beta, -alpha, -turnMultiplier)[1]
        scores.append(score)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                bestMove = move
        gs.undoMove()

        alpha = max(alpha, maxScore)
        if beta <= alpha:
            break

    return bestMove, maxScore

def miniMax(gs, depth, alpha, beta, maximizingPlayer, colorToMove):
    if depth == 0:
        return None, colorToMove * boardScore(gs)
    
    moveOrder = orderMoves(gs.getValidMoves())
    #moveOrder = gs.getValidMoves()
    bestMove = None

    if maximizingPlayer:
        maxScore = -10000
        for move in moveOrder:
            gs.makeMove(move)
            score = miniMax(gs, depth - 1, alpha, beta, False, -colorToMove)[1]

            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    bestMove = move
            gs.undoMove()

            alpha = max(alpha, maxScore)
            if beta <= alpha:
                break

        return bestMove, maxScore
    else:
        minScore = 10000
        for move in moveOrder:
            gs.makeMove(move)
            score = miniMax(gs, depth - 1, alpha, beta, True, colorToMove)[1]
            
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    bestMove = move
            gs.undoMove()

            beta = min(beta, minScore)
            if beta <= alpha:
                break

        return bestMove, minScore

def findBestMove(gs):
    global scores
    scores = []
    nextMove = None
    
    start = timer()
    #nextMove, score = negaMax(gs, DEPTH, -10000,  10000, 1 if gs.whiteToMove else -1)
    nextMove, score = miniMax(gs, DEPTH, -10000,  10000, True, 1 if gs.whiteToMove else -1)

    end = timer()
    print(sorted(scores))
    print("")
    print("Execution Time", round(end-start, 2), "seconds")
    print("")
    return nextMove

def MoveGenerationTest(gs, depth):
    if depth == 0:
        return 1
    numPositions = 0
    for move in gs.getValidMoves():
        gs.makeMove(move)
        numPositions += MoveGenerationTest(gs, depth -1)
        gs.undoMove()
    return numPositions


"""

> keep track of board for last 4 moves
> if board 1 == board 3, board 2 == board 4
> Random move for both sides

"""