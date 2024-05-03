"""
This is our main driver file. It will be responsible for 
	- handling user input
	- displaying current GameState object
"""
#Working with arguments to see which algorithm to use for the Chess Engine -> Basic, Advances;
import sys
import pygame as p
import ChessEngine
import EasyBot
import MediumBot
import HardBot
from Button import Button

p.init()

WIDTH = 1000
HEIGHT = 800
DIMENTION_WIDTH = 10	 # 8*8 CHESS BOARD
DIMENTION_HEIGHT = 8
SQ_SIZE_WIDTH = WIDTH // DIMENTION_WIDTH
SQ_SIZE_HEIGHT = HEIGHT // DIMENTION_HEIGHT
MAX_FPS = 15
IMAGES = {}

DIFFICULTY = ""
PLAYER_NUMBERS = 1

'''
Initialise the global dictionary of images. This will be called exactly once in the main
'''
def loadImages():
	pieces = ['bP', 'bR', 'bN', 'bC', 'bA', 'bB', 'bQ', 'bK', 'wP', 'wR', 'wN', 'wC', 'wA', 'wB', 'wQ', 'wK']
	for piece in pieces:
		IMAGES[piece] = p.transform.scale(p.image.load("assets/images/" + piece + ".png"), (SQ_SIZE_WIDTH, SQ_SIZE_HEIGHT))
	# Note: We can access a piece by saying IMAGES['wP'] -> will give white pawn; 

def menuOne(screen):
	bg = p.image.load("assets/images/StarsBackground.png")
	bg2 = p.image.load("assets/images/ChessBackground.png")
	while True:

		screen.fill("grey")
		screen.blit(bg, (0,0))

		MENU_MOUSE_POS = p.mouse.get_pos()

		BUTTON_ONE = Button(p.image.load("assets/buttons/StarWarsButton.png"), (500, 250))
		BUTTON_TWO = Button(p.image.load("assets/buttons/TraditionalButton.png"), (500, 550))

		#SCREEN.blit(MENU_TEXT, MENU_RECT)
		BUTTON_ONE.update(screen)
		BUTTON_TWO.update(screen)

		for event in p.event.get():
			if event.type == p.QUIT:
				p.quit()
				sys.exit()
			if event.type == p.MOUSEBUTTONDOWN:
				if BUTTON_ONE.checkForInput(MENU_MOUSE_POS):
					optionsSelected, difficulty, playerColour = menuTwo(screen, bg)
					return optionsSelected, difficulty, playerColour
				if BUTTON_TWO.checkForInput(MENU_MOUSE_POS):
					optionsSelected, difficulty, playerColour = menuTwo(screen, bg2)
					return optionsSelected, difficulty, playerColour
				
		p.display.update()

def menuTwo(screen, bg):

	while True:

		screen.fill("grey")
		if bg != None:
			screen.blit(bg, (0,0))

		MENU_MOUSE_POS = p.mouse.get_pos()

		BUTTON_ONE = Button(p.image.load("assets/buttons/OnePlayer.png"), (500, 250))
		BUTTON_TWO = Button(p.image.load("assets/buttons/TwoPlayer.png"), (500, 550))

		#SCREEN.blit(MENU_TEXT, MENU_RECT)
		BUTTON_ONE.update(screen)
		BUTTON_TWO.update(screen)

		for event in p.event.get():
			if event.type == p.QUIT:
				p.quit()
				sys.exit()
			if event.type == p.MOUSEBUTTONDOWN:
				if BUTTON_ONE.checkForInput(MENU_MOUSE_POS):
					optionsSelected, difficulty, playerColour = menuThree(screen, bg)
					return optionsSelected, difficulty, playerColour
				
				if BUTTON_TWO.checkForInput(MENU_MOUSE_POS):
					# Returning None as a two player game does not have an AI.
					# Also, the players would decide between themselves who is playing what colour
					# so the colour menu does not need to be shown.
					return True, None, None
				
		p.display.update()

def menuThree(screen, bg):

	while True:

		screen.fill("grey")
		if bg != None:
			screen.blit(bg, (0,0))

		MENU_MOUSE_POS = p.mouse.get_pos()

		BUTTON_ONE = Button(p.image.load("assets/buttons/BlackButton.png"), (500, 250))
		BUTTON_TWO = Button(p.image.load("assets/buttons/WhiteButton.png"), (500, 550))

		#SCREEN.blit(MENU_TEXT, MENU_RECT)
		BUTTON_ONE.update(screen)
		BUTTON_TWO.update(screen)

		for event in p.event.get():
			if event.type == p.QUIT:
				p.quit()
				sys.exit()
			if event.type == p.MOUSEBUTTONDOWN:
				if BUTTON_ONE.checkForInput(MENU_MOUSE_POS):
					optionsSelected, difficulty = menuFour(screen, bg)
					playerColour = False
					return optionsSelected, difficulty, playerColour
				
				if BUTTON_TWO.checkForInput(MENU_MOUSE_POS):
					optionsSelected, difficulty = menuFour(screen, bg)
					playerColour = True
					return optionsSelected, difficulty, playerColour

		p.display.update()

def menuFour(screen, bg):

	while True:

		screen.fill("grey")
		if bg != None:
			screen.blit(bg, (0,0))

		MENU_MOUSE_POS = p.mouse.get_pos()

		BUTTON_ONE = Button(p.image.load("assets/buttons/EasyButton.png"), (500, 150))
		BUTTON_TWO = Button(p.image.load("assets/buttons/MediumButton.png"), (500, 400))
		BUTTON_Three = Button(p.image.load("assets/buttons/HardButton.png"), (500, 650))

		#SCREEN.blit(MENU_TEXT, MENU_RECT)

		for button in [BUTTON_ONE, BUTTON_TWO, BUTTON_Three]:
			button.update(screen)

		for event in p.event.get():
			if event.type == p.QUIT:
				p.quit()
				sys.exit()
			if event.type == p.MOUSEBUTTONDOWN:
				if BUTTON_ONE.checkForInput(MENU_MOUSE_POS):
					return True, "E"
				if BUTTON_TWO.checkForInput(MENU_MOUSE_POS):
					return True, "M"
				if BUTTON_Three.checkForInput(MENU_MOUSE_POS):
					return True, "H"
					
		p.display.update()


'''
This will be out main driver. It will handle user input and update the graphics.
'''
def main():

	screen = p.display.set_mode((WIDTH, HEIGHT))
	clock = p.time.Clock()
	screen.fill(p.Color('white'))
	optionsSelected = False
	
	while not optionsSelected:
		optionsSelected, difficulty, playerColour = menuOne(screen)

	gs = ChessEngine.GameState()
	validMoves = gs.getValidMoves()		# get a list of valid moves.
	moveMade = False		 			# to check if the user made a move. If true recalculate validMoves.
	loadImages()						# only do this once -> before the while loop
	running = True
	animate = False		 				# Flag variable to note when we should animate the piece movement
	sqSelected = ()		 				# no sq is selected initially, keep track of the last click by the user -> (tuple : (row,col))
	playerClicks = []					# contains players clicks => [(6,4),(4,4)]  -> pawn at (6,4) moved 2 steps up on (4,4)
	playerOne = True					# if Human is playing white -> this will be true
	playerTwo = False					# if Human is playing black -> this will be true
	gameOver = False					# True in case of Checkmate and Stalemate
	numMoves = 0
	lastFourMoves = []
	AIMove = None


	while running:

		"""
		> if diff is none (2 player)
			> human turn is always true
		> if 1 player
			> human turn is true if white, else black
		
		"""
		if difficulty == None:
			humanTurn = True
		else:
			humanTurn = playerColour 
		
		print("humanTurn", humanTurn)
		for e in p.event.get():
			if e.type == p.QUIT:
				running = False
			#MOUSE HANDLERS
			elif e.type == p.MOUSEBUTTONDOWN:
				if not gameOver and humanTurn:
					location = p.mouse.get_pos()	 # (x,y) position of mouse
					col = location[0]//SQ_SIZE_WIDTH
					row = location[1]//SQ_SIZE_HEIGHT
					if sqSelected == (row, col): 	# user selected the same sq. twice -> deselect the selecion
						sqSelected = ()
						playerClicks = []
					else:
						sqSelected = (row, col)
						playerClicks.append(sqSelected)	 # append for both 1st and 2nd click
						if len(playerClicks) == 2: 	# when 2nd click
							move = ChessEngine.Move(playerClicks[0],playerClicks[1], gs.board)
							for i in range(len(validMoves)):

								if move == validMoves[i]:
									gs.makeMove(validMoves[i])
									moveMade = True
									animate = True
									playerClicks = [] 	# reset platerClicks
									sqSelected = () 	# reset user clicks

									numMoves += 1
							if not moveMade:
								playerClicks = [sqSelected]

			#KEY HANDLERS
			elif e.type == p.KEYDOWN:
				if e.key == p.K_z:		#undo last move id 'z' is pressed
					gs.undoMove() 
					moveMade = True	 	# can do `validMoves = gs.validMoves()` but then if we change function name we will have to change the call at various places.
				if e.key == p.K_r: 	#reset the game if 'r' is pressed
					gs = ChessEngine.GameState()
					sqSelected = ()
					playerClicks = []
					moveMade = False
					animate = False
					gameOver = False
					validMoves = gs.getValidMoves()

		# AI Move finder logic
		if not gameOver:
			if not humanTurn:
				if difficulty == "E":
					AIMove = EasyBot.findBestMove(gs)
				elif difficulty == "M":
					AIMove = MediumBot.findBestMove(gs)
				else:
					AIMove = HardBot.findBestMove(gs)

				if AIMove is None:
					AIMove = MediumBot.randomMove(validMoves)
				gs.makeMove(AIMove)

				moveMade = True
				animate = True
				"""
			
		if not gameOver and not humanTurn :
			
			AIMove = HardBot.findBestMove(gs)"""
			"""
			if AIMove is None:
				AIMove = MediumBot.randomMove(validMoves)
			
			if len(lastFourMoves) < 4:
				lastFourMoves.append(gs.board)
			elif lastFourMoves[0] == "h":
				AIMove = MediumBot.randomMove(validMoves)
				lastFourMoves = []
			elif (lastFourMoves[0] == lastFourMoves[2]) and (lastFourMoves[1] == lastFourMoves[3]):
				AIMove = MediumBot.randomMove(validMoves)
				lastFourMoves = ["h"]
			else:
				lastFourMoves = []

			gs.makeMove(AIMove)

			numMoves += 1
			"""
			

		if moveMade:
			playerColour = not playerColour
			if len(gs.moveLog) > 0 and animate:
				animate = False
				animateMove(gs.moveLog[-1], screen, gs.board, clock)
			validMoves = gs.getValidMoves()
			moveMade = False
		drawGameState(screen, gs, sqSelected, validMoves)

		if gs.checkMate:
			gameOver = True

			if gs.whiteToMove:
				drawText(screen, "Black Won by Checkmate!");
			else:
				drawText(screen, "White Won by Checkmate!");

		if gs.staleMate:
			gameOver = True
			drawText(screen, "Draw due to Stalemate!");
		clock.tick(MAX_FPS) 
		p.display.flip()


'''
For highlighting the correct sq. of selected piece and the squares it can move to
'''
def highlightSquares(screen, gs, selectedSquare, validMoves):
	if selectedSquare != ():
		r, c = selectedSquare
		enemyColor = 'b' if gs.whiteToMove else 'w'
		allyColor = 'w' if gs.whiteToMove else 'b'
		if gs.board[r][c][0] == allyColor:
			#Highlighting the selected Square
			s = p.Surface((SQ_SIZE_WIDTH, SQ_SIZE_HEIGHT))
			s.set_alpha(100)		# transparency value -> 0 : 100% transparent | 255 : 100% Opaque
			s.fill(p.Color('blue'))
			screen.blit(s, (c*SQ_SIZE_WIDTH, r*SQ_SIZE_HEIGHT))

			#Highlighting the valid move squares
			s.fill(p.Color('yellow'))
			for move in validMoves:
				if move.startRow == r and move.startCol == c:
					endRow = move.endRow
					endCol = move.endCol
					#if gs.board[endRow][endCol] == '--' or gs.board[endRow][endCol][0] == enemyColor:
					screen.blit(s, (endCol * SQ_SIZE_WIDTH, endRow * SQ_SIZE_HEIGHT))


'''
responsible for all the graphics in the game
'''
def drawGameState(screen, gs, selectedSquare, validMoves):
	drawBoard(screen) #draw squares on board (should be called before drawing anything else)
	highlightSquares(screen, gs, selectedSquare, validMoves)
	drawPieces(screen, gs.board) #draw pieces on the board


'''
draw the squares on the board
'''
def drawBoard(screen):
	global colors
	colors = [p.Color(235, 235, 208), p.Color(119, 148, 85)]
	for r in range(DIMENTION_HEIGHT):
		for c in range(DIMENTION_WIDTH):
			color = colors[(r+c)%2]
			p.draw.rect(screen, color, p.Rect(SQ_SIZE_HEIGHT*c, SQ_SIZE_WIDTH*r , SQ_SIZE_HEIGHT, SQ_SIZE_WIDTH))



'''
draw the pieces on the board using ChessEngine.GameState.board.
'''
def drawPieces(screen, board):
	for r in range(DIMENTION_HEIGHT):
		for c in range(DIMENTION_WIDTH):
			piece = board[r][c]
			if piece != '--':
				screen.blit(IMAGES[piece], p.Rect(SQ_SIZE_WIDTH*c, SQ_SIZE_HEIGHT*r , SQ_SIZE_WIDTH, SQ_SIZE_HEIGHT))


'''
Animates the movement of piece
'''
def animateMove(move, screen, board, clock):
	global colors
	dR = move.endRow - move.startRow
	dC = move.endCol - move.startCol
	framesPerSquare = 5		# frames to move 1 square
	frameCount = (abs(dR) + abs(dC)) * framesPerSquare
	for frame in range(frameCount + 1):
		r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
		drawBoard(screen)
		drawPieces(screen, board)
		#erase piece from endRow, endCol
		color = colors[(move.endRow + move.endCol) % 2]
		endSqaure = p.Rect(move.endCol * SQ_SIZE_WIDTH, move.endRow * SQ_SIZE_HEIGHT, SQ_SIZE_WIDTH, SQ_SIZE_HEIGHT)
		p.draw.rect(screen, color, endSqaure)
		#draw captured piece back
		# if move.pieceCaptured != '--':
			# screen.blit(IMAGES[move.pzieceCaptured], endSqaure)
		#draw moving piece
		screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE_WIDTH, r*SQ_SIZE_HEIGHT, SQ_SIZE_WIDTH, SQ_SIZE_HEIGHT))
		p.display.flip()
		clock.tick(60)

'''
To wrtie some text in the middle of the screen!
'''
def drawText(screen, text):
						#  Font Name  Size Bold  Italics
	font = p.font.SysFont("Helvitica", 32, True, False)
	textObject = font.render(text, 0, p.Color('Blue'))
	textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
	screen.blit(textObject, textLocation)

if __name__ == '__main__':
	main()





























