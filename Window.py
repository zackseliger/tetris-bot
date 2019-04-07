import pygame
import random
import math

config = {
    'cell_size': 30,
    'cols': 10,
    'rows': 20,
    'delay': 750,
    'maxfps': 60
}

class Tetromino(object):
    def __init__(self, type):
        self.type = type
        self.points = []
        c = 5  # c for center
        self.rotationState = 0

        if self.type == 1:#'I'
            self.points.append((0, c))
            self.points.append((0,c+1))
            self.points.append((0, c - 2))
            self.points.append((0, c - 1))
        elif self.type == 2:#'O'
            self.points.append((0,c))
            self.points.append((0,c+1))
            self.points.append((-1,c))
            self.points.append((-1,c+1))
        elif self.type == 3:#'S'
            self.points.append((0,c))
            self.points.append((0,c-1))
            self.points.append((-1,c))
            self.points.append((-1,c+1))
        elif self.type == 4:#'Z'
            self.points.append((0,c))
            self.points.append((0,c+1))
            self.points.append((-1,c))
            self.points.append((-1,c-1))
        elif self.type == 5:#'J'
            self.points.append((0,c))
            self.points.append((0,c+1))
            self.points.append((0,c-1))
            self.points.append((-1,c-1))
        elif self.type == 6:#'L'
            self.points.append((0,c))
            self.points.append((0,c-1))
            self.points.append((0,c+1))
            self.points.append((-1,c+1))
        elif self.type == 7:#'T'
            self.points.append((-1,c))
            self.points.append((-1,c-1))
            self.points.append((-1,c+1))
            self.points.append((0,c))


    def getPoints(self):
        return self.points

    # moves tetromino down by amt, with error checking
    def moveDown(self, amt):
        # if already at bottom, can't go further down
        for i in range(len(self.points)):
            if self.points[i][1]+amt > config['rows']:
                return

        for i in range(len(self.points)):
            self.points[i] = (self.points[i][0]+amt, self.points[i][1])

    # moves tetromino to the side by amt, with error checking
    def moveX(self, amt):
        for i in range(len(self.points)):
            self.points[i] = (self.points[i][0], self.points[i][1]+amt)

        # check bounds and reverse if overstepped
        for point in self.points:
            if point[1] < 0 or point[1] >= config['cols']:
                for i in range(len(self.points)):
                    self.points[i] = (self.points[i][0], self.points[i][1] - amt)
                return

    def getState(self):
        return [self.points.copy(), self.rotationState, self.type]

    def setState(self, state):
        self.points = state[0]
        self.rotationState = state[1]
        self.type = state[2]

    # rotates tetronimo
    def rotate(self, times):
        # some shapes only get rotated in some ways
        if self.type == 2:
            return
        if self.type == 1 and self.points[0][0] != self.points[0][0]:
            c = self.points[0][1]
            self.points = []
            self.rotationState = 0
            self.points.append((0, c))
            self.points.append((0, c + 1))
            self.points.append((0, c - 2))
            self.points.append((0, c - 1))
            return

        # update rotation state
        self.rotationState += times
        if self.rotationState > 3 or self.rotationState < 0:
            self.rotationState = self.rotationState % 4

        # use first point as center point
        centerR = self.points[0][0]
        centerC = self.points[0][1]

        for i in range(len(self.points)):
            if i != 0:
                # get distance and angle from center
                distanceR = centerR - self.points[i][0]
                distanceC = centerC - self.points[i][1]
                radius = math.hypot(distanceC, distanceR)
                angle = math.atan2(distanceR, distanceC)
                # subtract 45 degrees (clockwise) to angle to calculate each points' new location
                angle -= math.pi/2 * times
                new_r = round(radius*math.sin(angle))
                new_c = round(radius*math.cos(angle))
                self.points[i] = (new_r+centerR, new_c+centerC)

class Window(object):
    def __init__(self):
        self.running = True
        self.screen = pygame.display.set_mode((500, 600))
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(1, 125)
        # slow timer here
        self.slowTimer = 0
        self.mustMoveDown = True
        # initializing board
        self.fallingPiece = Tetromino(random.randint(1,7))
        self.board = []
        self.score = 0
        self.gameOver = False
        self.font = pygame.font.SysFont('Arial', 24)
        self.scoreGUIText = self.font.render("Score:", True, (255, 255, 255))
        self.overGUIText = self.font.render("Game Over", True, (255, 255, 255), (0,0,0))
        self.scoreText = self.font.render(str(self.score), True, (255, 255, 255))
        for r in range(config['rows']):
            self.board.append([])
            for c in range(config['cols']):
                self.board[r].append(0)

    def update(self):
        # sleeping to the tune of 'maxfps' fps
        self.clock.tick(config['maxfps'])

        # is game over?
        if self.isGameOver():
            self.gameOver = True

        # handling events
        for event in pygame.event.get():
            # quit signal sent by hitting 'x' or something
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and self.fallingPiece is not None:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.fallingPiece.moveX(1)
                    # prevents piece from moving through other pieces
                    if self.isPieceDoneFalling(self.fallingPiece):
                        self.fallingPiece.moveX(-1)
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.fallingPiece.moveX(-1)
                    # prevents piece from moving through other pieces
                    if self.isPieceDoneFalling(self.fallingPiece):
                        self.fallingPiece.moveX(1)
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.fallingPiece.moveDown(1)
                    self.solidifyPieceIfNecessary()
                    self.mustMoveDown = False
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
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
        if piece.type == 0:
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
            for point in self.fallingPiece.getPoints():
                self.board[point[0]][point[1]] = 1
            self.fallingPiece = None
            # gotta do this
            self.checkAndRemoveTetris()

    def isGameOver(self):
        isOver = False
        for c in range(len(self.board[0])):
            if self.board[0][c] != 0:
                isOver = True
                break
        return isOver

    def checkAndRemoveTetris(self):
        fullRows = []
        # get index of rows that are full
        for i in range(len(self.board)):
            isCleared = True
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    isCleared = False
                    continue
            if isCleared:
                fullRows.append(i)

        # add score based on full rows, also update drawing
        numRows = len(fullRows)
        if numRows == 1:
            self.score += 40
        elif numRows == 2:
            self.score += 100
        elif numRows == 3:
            self.score += 300
        elif numRows == 4:
            self.score += 1200
        self.scoreText = self.font.render(str(self.score), True, (255, 255, 255))

        # delete full rows and add blank rows at top
        for i in range(len(fullRows)):
            self.board.pop(fullRows[i])
            for j in range(len(fullRows)):
                if i != j and fullRows[i] > fullRows[j]:
                    fullRows[j] += 1

            self.board.insert(0, [])
            for c in range(config['cols']):
                self.board[0].append(0)

    # returns true if piece is at bottom or colliding with any other tile
    # also, for collision purposes, if any piece are left or right of the board
    def isPieceDoneFalling(self, tetromino):
        for point in tetromino.getPoints():
            if point[0] >= config['rows']:
                return True
            elif point[1] < 0 or point[1] >= config['cols']:
                return True
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] != 0:
                    for point in tetromino.getPoints():
                        if r == point[0] and c == point[1]:
                            return True
        return False

    def draw(self):
        self.screen.fill((0,0,0))

        # drawing the board
        if self.fallingPiece is not None:
            fallingPoints = self.fallingPiece.getPoints()
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                # drawing the currently falling piece
                fallingPoint = False
                if self.fallingPiece is not None:
                    for point in fallingPoints:
                        if r == point[0] and c == point[1]:
                            pygame.draw.rect(self.screen, (50, 125, 50), [c * config['cell_size'], r * config['cell_size'], config['cell_size'], config['cell_size']])
                            fallingPoint = True
                # logic for drawing established pieces and background tiles
                if fallingPoint == False:
                    if self.board[r][c] != 0:
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
window = Window()
# main game loop
while window.running:
    window.update()
    window.draw()