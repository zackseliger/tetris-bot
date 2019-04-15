import pygame
import random
from Tetromino import Tetromino
from Settings import *
from Board import Board
from Player import *

class Window:

    def __init__(self, player):
        self.running = True
        self.screen = pygame.display.set_mode((500, 600))
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(1, 125)
        # slow timer here
        self.slowTimer = 0
        self.mustMoveDown = True
        # initializing board
        self.fallingPiece = Tetromino(random.randint(1,7))
        self.board = Board()
        self.score = 0
        self.gameOver = False
        self.font = pygame.font.SysFont('Arial', 24)
        self.scoreGUIText = self.font.render("Score:", True, (255, 255, 255))
        self.overGUIText = self.font.render("Game Over", True, (255, 255, 255), (0,0,0))
        self.scoreText = self.font.render(str(self.score), True, (255, 255, 255))
        self.player = player

    def update(self):
        # sleeping to the tune of 'maxfps' fps
        self.clock.tick(config['maxfps'])

        # update the player (checks on our seperate thread)
        self.player.update()

        # is game over?
        if self.isGameOver():
            self.gameOver = True

        # handling events
        for event in pygame.event.get():
            # quit signal sent by hitting 'x' or something
            if event.type == pygame.QUIT:
                self.running = False
            if self.fallingPiece is not None:
                # moving piece if we've recieved corresponding events
                if event.type == userEventTypes['right']:
                    self.fallingPiece.moveX(1)
                    # prevents piece from moving through other pieces
                    if self.isPieceDoneFalling(self.fallingPiece):
                        self.fallingPiece.moveX(-1)
                elif event.type == userEventTypes['left']:
                    self.fallingPiece.moveX(-1)
                    # prevents piece from moving through other pieces
                    if self.isPieceDoneFalling(self.fallingPiece):
                        self.fallingPiece.moveX(1)
                elif event.type == userEventTypes['down']:
                    self.fallingPiece.moveDown(1)
                    self.solidifyPieceIfNecessary()
                    self.mustMoveDown = False
                elif event.type == userEventTypes['rotate']:
                    self.rotatePiece(self.fallingPiece)
        if self.gameOver:
            return
        # moving pieces down and checking for finalizing piece position
        self.slowTimer += 1
        if self.slowTimer < 60:
            return
        self.slowTimer = 0
        # if fallingPiece is none, make a new falling piece
        if self.fallingPiece is None:
            self.fallingPiece = Tetromino(random.randint(1,7))
        # move piece down if not moved down before
        if self.mustMoveDown:
            self.fallingPiece.moveDown(1)
        else:
            self.mustMoveDown = True
        # add piece to board and if it did, check for cleared rows
        self.solidifyPieceIfNecessary()

    def rotatePiece(self, piece):
        if piece.type == 2:
            return
        
        # get original state in case test cases don't work
        originalState = piece.getState()
        piece.rotate(1)
        tests = []

        # get tests cases for rotation correction
        if piece.type == 1:
            if piece.rotationState == 0:
                tests = [(-1,0)] 
            elif piece.rotationState == 1:
                tests = [(-1,0), (0,1)]
        else:
            if piece.rotationState == 1:
                tests = [(1,0), (1,-1), (0,2), (1,2)]
            elif piece.rotationState == 3:
                tests = [(-1, 0), (-1, -1), (0, 2), (-1, 2)]

        # run through test cases for piece
        for testTuple in tests:
            if not (self.isPieceDoneFalling(piece)):
                break
            piece.moveDown(-testTuple[1])
            piece.moveX(testTuple[0])

        # if no test cases work, undo rotation
        if self.isPieceDoneFalling(piece):
            piece.setState(originalState)

    def solidifyPieceIfNecessary(self):
        # solidifying piece
         if self.isPieceDoneFalling(self.fallingPiece):
            self.fallingPiece.moveDown(-1)
            self.board.make_move(self.fallingPiece)
            self.fallingPiece = None
            # gotta do this
            self.checkAndRemoveTetris()

    def isGameOver(self):
        """Returns whether board is terminal"""
        return self.board.is_terminal()

    def checkAndRemoveTetris(self):
        """uses check tetris and updates score based on output"""
        numRows = self.board.check_tetris()
        if numRows == 1:
            self.score += 40
        elif numRows == 2:
            self.score += 100
        elif numRows == 3:
            self.score += 300
        elif numRows == 4:
            self.score += 1200
        self.scoreText = self.font.render(str(self.score), True, (255, 255, 255))

    # returns true if piece is at bottom or colliding with any other tile
    # also, for collision purposes, if any piece are left or right of the board
    def isPieceDoneFalling(self, tetromino):
        return self.board.is_piece_done_falling(tetromino)

    def draw(self):
        self.screen.fill((0,0,0))
        board_array = self.board.get_board()
        # drawing the board
        if self.fallingPiece is not None:
            fallingPoints = self.fallingPiece.getPoints()
        for r in range(len(board_array)):
            for c in range(len(board_array[r])):
                # drawing the currently falling piece
                fallingPoint = False
                if self.fallingPiece is not None:
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
window = Window(HumanPlayer())
# main game loop
while window.running:
    window.update()
    window.draw()
