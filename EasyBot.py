import random
from timeit import default_timer as timer

DEPTH = 2
PIECE_VALUES = {'P': 10, 'N': 30, 'B': 30, 'R':50, 'A': 70, 'C': 80, 'Q': 90, 'K': 1000}
STALEMATE = 0 

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

def boardScore(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -1000   # Black is the winner (Negative is in favour of black)
        else:
            return 1000 # White is the winner
        
    score = 0
    for row in gs.board:
        for square in row:
            # If the square is white then add the value of the piece on it
            if square[0] == 'w':
                score += PIECE_VALUES[square[1]]
            # If the square is black then subtract the value of the piece on it
            elif square[0] == 'b':
                score -= PIECE_VALUES[square[1]]
    return score

def miniMax(gs, depth, maximizingPlayer, colorToMove):
    if depth == 0:
       return None, colorToMove * boardScore(gs)
    
    bestMove = None
    if maximizingPlayer:
        maxScore = -1000
        for move in gs.getValidMoves():
            gs.makeMove(move)
            score = miniMax(gs, depth - 1, False, - colorToMove)[1]
            
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    bestMove = move
            gs.undoMove()

        return bestMove, maxScore
    else:
        minScore = 1000
        for move in gs.getValidMoves():
            gs.makeMove(move)
            score = miniMax(gs, depth - 1, True, colorToMove)[1]

            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    bestMove = move
            gs.undoMove()

        return bestMove, minScore
    
   
def findBestMove(gs):

    n = random.randrange(0, 100)
    bestMove = None
    if n < 80:
        start = timer()
        bestMove, score = miniMax(gs, DEPTH,  True, 1 if gs.whiteToMove else -1)
        end = timer()

        print("")
        print("Execution Time", round(end-start, 2), "seconds")
        print("")
    
    return bestMove

def MoveGenerationTest(gs, depth):
    if depth == 0:
        return 1
    numPositions = 0
    for move in gs.getValidMoves():
        gs.makeMove(move)
        numPositions += MoveGenerationTest(gs, depth -1)
        gs.undoMove()
    return numPositions