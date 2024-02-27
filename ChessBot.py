import random

DEPTH = 1

def randomMove(validMoves):
    print("aaaaa")
    return validMoves[random.randint(0, len(validMoves) - 1)]

def evaluatePosition(board, color):

    score = 0
    pieceValues = {'P': 10, 'N': 30, 'B': 30, 'R':50, 'A': 70, 'C': 80, 'Q': 90, 'K': 1000}
    for r in range(len(board)):
            for c in range(len(board[r])):
                 square = board[r][c]
                 if square != "--":
                    if square[0] == color:
                        score += pieceValues[square[1]]
                    else:
                         score -= pieceValues[square[1]]

    return score

def minimax(gs, depth, validMoves, isMaxPlayer):
    if depth == 0:
        if isMaxPlayer:
            return evaluatePosition(gs.board, 'w')
        else:
            return evaluatePosition(gs.board, 'b')
    global nextMove 
    if isMaxPlayer:
        maxScore = - 1000
        for move in validMoves:
            gs.makeMove(move)
            nextMovesBranch = gs.getValidMoves()
            score = minimax(gs, depth -1, nextMovesBranch, False)

            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = 1000
        for move in validMoves:
            gs.makeMove(move)
            nextMovesBranch = gs.getValidMoves()
            score = minimax(gs, depth -1, nextMovesBranch, True)

            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore
    
     
def findBestMove(gs, validMoves):
    global nextMove 
    nextMove = None
    minimax(gs, DEPTH, validMoves,  True)
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