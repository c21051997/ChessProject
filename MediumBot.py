import random
from timeit import default_timer as timer


DEPTH = 3
PIECE_VALUES = {'P': 10, 'N': 30, 'B': 30, 'R':50, 'A': 70, 'C': 80, 'Q': 90, 'K': 1000}
STALEMATE = 0 

def randomMove(validMoves):
    print("aaaaa")
    return validMoves[random.randint(0, len(validMoves) - 1)]

def evaluatePosition(gs):
    score = 0

    for row in gs.board:
            for square in row:
                 if square != "--":
                    if square[0] == 'b':
                        score += PIECE_VALUES[square[1]]
                    else:
                         score -= PIECE_VALUES[square[1]]

    return score

def evaluatePosition2(gs, maxPlayer, whiteToMove):
    score = 0

    for row in gs.board:
            for square in row:
                 if square != "--":
                    pieceColor = square[0]
                    pieceType = square[1]
                    if maxPlayer and whiteToMove:
                        if pieceColor == 'w':
                            score += PIECE_VALUES[pieceType]
                        else: 
                            score -= PIECE_VALUES[pieceType]
                    else:
                        score -= PIECE_VALUES[pieceType]
    return score


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

def quiesce(gs, alpha, beta):
    standPat = evaluatePosition(gs)
    if standPat >= beta:
        return beta
    if alpha < standPat:
        alpha = standPat
    pass



def boardScore(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -1000   # BLACK WINS
        else:
            return 1000
        
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += PIECE_VALUES[square[1]]
            elif square[0] == 'b':
                score -= PIECE_VALUES[square[1]]
    return score

def findMoveNegaMaxAlphaBetaPruning(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * boardScore(gs)

    # Traverse better moves 1st -> ones with checks and captures -> will lead to more pruning and more optimised algorithm
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBetaPruning(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)   # negative for NEGA Max
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

def negaMax(gs, depth, alpha, beta, turnMultiplier):
    if depth == 0:
        return None, turnMultiplier * boardScore(gs)
        
    moveOrder = orderMoves(gs.getValidMoves())
    if (len(gs.getValidMoves()) != len(moveOrder)):
        print("hey")
    bestMove = None

    maxScore = -1000
    for move in moveOrder:
        gs.makeMove(move)
        score = -negaMax(gs, depth - 1, -beta, -alpha, -turnMultiplier)[1]
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
    
    #moveOrder = orderMoves(gs.getValidMoves())
    moveOrder = gs.getValidMoves()
    bestMove = None

    if maximizingPlayer:
        maxScore = -1000
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
        minScore = 1000
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
    
    nextMove = None
    allScores = []
    start = timer()
    nextMove, score = negaMax(gs, DEPTH, -1000,  1000, 1 if gs.whiteToMove else -1)
    #nextMove, score = miniMax(gs, DEPTH, -1000,  1000, True, 1 if gs.whiteToMove else -1)
    end = timer()
    print("")
    print("Execution Time", round(end-start, 2), "seconds")
    print("")
    return nextMove
    """
    start = timer()
    global nextMove     # to find the next move
    nextMove = None
    findMoveNegaMaxAlphaBetaPruning(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1) 
    end = timer()
    print(end-start)
    return nextMove"""

def MoveGenerationTest(gs, depth):
    if depth == 0:
        return 1
    numPositions = 0
    for move in gs.getValidMoves():
        gs.makeMove(move)
        numPositions += MoveGenerationTest(gs, depth -1)
        gs.undoMove()
    return numPositions