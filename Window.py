import pygame
from Settings import *
from Board import Board
from Player import *


class Window:
    def __init__(self, player):
        """initalizes the screen and clock from pygame, the text
        slows down player to avoid too much updating
        initializes the player, the board"""
        self.running = True
        self.screen = pygame.display.set_mode((500, 600))
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(1, 125)
        # slow timer here
        self.slowTimer = 0
        self.mustMoveDown = True
        # initializing board
        self.board = Board()
        self.score = 0
        self.gameOver = False
        self.font = pygame.font.SysFont('Arial', 24)
        self.scoreGUIText = self.font.render("Score:", True, (255, 255, 255))
        self.overGUIText = self.font.render("Game Over", True, (255, 255, 255), (0,0,0))
        self.scoreText = self.font.render(str(self.score), True, (255, 255, 255))
        self.player = player
        self.player.setBoard(self.board)

    def update(self):
        """Handles the update of the board and falling piece for this thread"""
        # sleeping to the tune of 'maxfps' fps
        self.clock.tick(config['maxfps'])

        # update the player (checks on our seperate thread)
        self.player.update()

        # is game over?
        if self.board.isTerminal():
            self.gameOver = True

        # handling events
        for event in pygame.event.get():
            # quit signal sent by hitting 'x' or something
            if event.type == pygame.QUIT:
                self.running = False
            if self.board.fallingPiece is not None:
                # moving piece if we've recieved corresponding events
                if event.type == userEventTypes['rotate']:
                    self.board.rotatePiece()
                elif event.type == userEventTypes['right']:
                    self.board.fallingPiece.moveX(1)
                    # prevents piece from moving through other pieces
                    if self.board.isPieceDoneFalling():
                        self.board.fallingPiece.moveX(-1)
                elif event.type == userEventTypes['left']:
                    self.board.fallingPiece.moveX(-1)
                    # prevents piece from moving through other pieces
                    if self.board.isPieceDoneFalling():
                        self.board.fallingPiece.moveX(1)
                elif event.type == userEventTypes['down']:
                    self.board.fallingPiece.moveDown(1)
                    self.solidifyPieceIfNecessary()
                    self.mustMoveDown = False
        if self.gameOver:
            return
        # moving pieces down and checking for finalizing piece position
        self.slowTimer += 1
        if self.slowTimer < 5:
            return
        self.slowTimer = 0
        # if fallingPiece is none, make a new falling piece
        if self.board.fallingPiece is None:
            self.board.makeNewPiece()
        # move piece down if not moved down before
        if self.mustMoveDown:
            self.board.fallingPiece.moveDown(1)
        else:
            self.mustMoveDown = True
        # add piece to board and if it did, check for cleared rows
        self.solidifyPieceIfNecessary()

    def solidifyPieceIfNecessary(self):
        """Given that the piece is done falling,
        moves the piece back up to no longer overlap with pre-placed,
        updates board with piece's squares, removes fallingPiece"""
        # solidifying piece
        if self.board.isPieceDoneFalling():
            self.board.fallingPiece.moveDown(-1)
            self.board.makeMove()
            self.board.fallingPiece = None
            # gotta do this
            self.checkAndRemoveTetris()

    def checkAndRemoveTetris(self):
        """uses checkTetris to remove the number of full rows
         and updates score based on number of removed rows"""
        numRows = self.board.checkTetris()
        if numRows == 1:
            self.score += 40
        elif numRows == 2:
            self.score += 100
        elif numRows == 3:
            self.score += 300
        elif numRows == 4:
            self.score += 1200
        self.scoreText = self.font.render(str(self.score), True, (255, 255, 255))

    def draw(self):
        """draws representaiton of board and falling piece through pygame"""
        self.screen.fill((0, 0,0))
        board_array = self.board.getBoard()
        # drawing the board
        fallingPiece = None
        if self.board.fallingPiece is not None:
            fallingPiece = self.board.fallingPiece
            fallingPoints = self.board.fallingPiece.getPoints()
        for r in range(len(board_array)):
            for c in range(len(board_array[r])):
                # drawing the currently falling piece
                fallingPoint = False
                if fallingPiece is not None:
                    for point in fallingPoints:
                        if r == point[0] and c == point[1]:
                            pygame.draw.rect(self.screen, (50, 125, 50), [c * config['cell_size'], r * config['cell_size'], config['cell_size'], config['cell_size']])
                            fallingPoint = True
                # logic for drawing established pieces and background tiles
                if fallingPoint == False:
                    if board_array[r][c] != 0:
                        pygame.draw.rect(self.screen, (125, 50, 50), [c * config['cell_size'], r * config['cell_size'], config['cell_size'], config['cell_size']])
                    elif (r+c) % 2 == 0:
                        pygame.draw.rect(self.screen, (50,50,50), [c*config['cell_size'],r*config['cell_size'],config['cell_size'],config['cell_size']])

        # text and gui stuff
        self.screen.blit(self.scoreGUIText, (350, 50))
        self.screen.blit(self.scoreText, (350, 100))
        if self.gameOver:
            self.screen.blit(self.overGUIText, (200, 250))

        pygame.display.flip()


# initializing our window
pygame.init()
"""WHERE TO EDIT TO CHANGE PLAYER
    HumanPlayer()   ZackPlayer()    YifanPlayer()    DrewPlayer()"""
window = Window(YifanPlayer())
# main game loop
while window.running:
    window.update()
    window.draw()
