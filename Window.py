import pygame
import random

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

        if self.type == 1:#'I'
            self.points.append((-1,c-2))
            self.points.append((-1,c-1))
            self.points.append((-1,c))
            self.points.append((-1,c+1))
        elif self.type == 2:#'O'
            self.points.append((-1,c))
            self.points.append((-1,c+1))
            self.points.append((-2,c))
            self.points.append((-2,c+1))
        elif self.type == 3:#'S'
            self.points.append((-1,c-1))
            self.points.append((-1,c))
            self.points.append((-2,c))
            self.points.append((-2,c+1))
        elif self.type == 4:#'Z"
            self.points.append((-1,c+1))
            self.points.append((-1,c))
            self.points.append((-2,c-1))
            self.points.append((-2,c))
        elif self.type == 5:#'L"
            self.points.append((-1,c-1))
            self.points.append((-1,c))
            self.points.append((-1,c+1))
            self.points.append((-2,c-1))
        elif self.type == 6:#'J"
            self.points.append((-1,c-1))
            self.points.append((-1,c))
            self.points.append((-1,c+1))
            self.points.append((-2,c+1))
        elif self.type == 7:#'T"
            self.points.append((-1,c))
            self.points.append((-2,c-1))
            self.points.append((-2,c))
            self.points.append((-2,c+1))


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

    # rotates tetronimo
    #def rotate(self):
        #if self.type == 1:

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
        for r in range(config['rows']):
            self.board.append([])
            for c in range(config['cols']):
                self.board[r].append(0)

    def update(self):
        # sleeping to the tune of 'maxfps' fps
        self.clock.tick(config['maxfps'])
        # handling events
        for event in pygame.event.get():
            # quit signal sent by hitting 'x' or something
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and self.fallingPiece is not None:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.fallingPiece.moveX(1)
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.fallingPiece.moveX(-1)
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.fallingPiece.moveDown(1)
                    self.solidifyPieceIfNecessary()
                    self.mustMoveDown = False
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.fallingPiece.rotate()
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
        self.solidifyPieceIfNecessary()

    def solidifyPieceIfNecessary(self):
        # solidifying piece
         if self.isPieceDoneFalling(self.fallingPiece):
            self.fallingPiece.moveDown(-1)
            for point in self.fallingPiece.getPoints():
                self.board[point[0]][point[1]] = 1
            self.fallingPiece = None

    def isPieceDoneFalling(self, tetromino):
        for point in tetromino.getPoints():
            if point[0] >= config['rows']:
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
        if self.fallingPiece is not None:
            fallingPoints = self.fallingPiece.getPoints()
        # drawing our board
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
        pygame.display.flip()

# initializing our window
pygame.init()
window = Window()
# main game loop
while window.running:
    window.update()
    window.draw()

# to quit
# pygame.display.quit