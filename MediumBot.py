import random

DEPTH = 5
PIECE_VALUES = {'P': 10, 'N': 30, 'B': 30, 'R':50, 'A': 70, 'C': 80, 'Q': 90, 'K': 1000}

def randomMove(validMoves):
    print("aaaaa")
    return validMoves[random.randint(0, len(validMoves) - 1)]

def evaluatePosition(gs):
    score = 0

    for row in gs.board:
            for square in row:
                 if square != "--":
                    if square[0] == 'w':
                        score += PIECE_VALUES[square[1]]
                    else:
                         score -= PIECE_VALUES[square[1]]

    return score

def negaMax(gs, depth, alpha, beta, turnColor):
    if depth == 0:
        return turnColor * evaluatePosition(gs)
    bestScore = -10000
    global bestMove
    bestMove = None

    for move in gs.getValidMoves():
        gs.makeMove(move)
        score = -negaMax(gs, depth - 1, -beta, -alpha, -turnColor)
        gs.undoMove()
        """if score >= beta:
            return score"""
        if score > bestScore:
            bestScore = score
            bestMove = move
        alpha = max(alpha, bestScore)
        if alpha >= beta:
            break

    return bestScore

def miniMax(gs, depth, alpha, beta, maximizingPlayer):
    if depth == 0:
        if maximizingPlayer:
            return evaluatePosition(gs)
        else:
            return - evaluatePosition(gs)
        
    if maximizingPlayer:
        maxScore = -10000
        for move in gs.getValidMoves():
            gs.makeMove(move)
            if gs.checkMate and depth == DEPTH:
                return move
            score = miniMax(gs, depth - 1, alpha, beta, False)
            gs.undoMove()
            if score > maxScore:
                maxScore = score
                bestMove = move

            alpha = max(alpha, maxScore)
            if beta <= alpha:
                break
        if depth == DEPTH:
            return maxScore, bestMove
        else:
            return maxScore
    else:
        minScore = 10000
        for move in gs.getValidMoves():
            gs.makeMove(move)
            if gs.checkMate and depth == DEPTH:
                return move
            score = miniMax(gs, depth - 1, alpha, beta, True)
            gs.undoMove()
            if score < minScore:
                minScore = score
                bestMove = move
            beta = min(beta, minScore)
            if beta <= alpha:
                break
                
        if depth == DEPTH:
            return minScore, bestMove
        else:
            return minScore

def findBestMove(gs):
    nextMove = None
    if gs.whiteToMove:
        turnColor = 1
    else:
        turnColor = -1
    score, nextMove = miniMax(gs, DEPTH, -10000,  10000, gs.whiteToMove)
    print(score)
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