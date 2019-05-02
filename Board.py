# Board for Tetris
from Settings import config
from Tetromino import *
import random
import math


class Board:
    def __init__(self, state=None):
        """initializes board as empty or thru eval of given state, bag
        (to cycle thru), size (from given Settings class), fallingPiece (new Tetromino)"""
        self.board = []
        self.size = config["rows"], config["cols"]
        self.bag = [1, 2, 3, 4, 5, 6, 7]
        self.fallingPiece = None
        self.makeNewPiece()
        for r in range(self.size[0]):
            self.board.append([])
            for c in range(self.size[1]):
                self.board[r].append(0)
        if state is not None:
            # state is string rep filled squares
            for i in range(len(state)):
                # row = i / size[0], col = i % size[1]
                if state[i] == "1":
                    self.board[math.floor(i / self.size[1])][(i % self.size[1])] = 1

    def getBoard(self):
        """Returns the array representation of the game board"""
        return self.board

    def getState(self):
        """returns the string representation of the game board"""
        state = ""
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                state += str(self.board[row][col])
        return state

    def makeCopy(self):
        """Copies the Board exactly, without being a reference to the original"""
        result = Board(self.getState())
        pieceState = self.fallingPiece.getState()
        newPiece = Tetromino(pieceState[2])
        newPiece.setState(pieceState)
        result.fallingPiece = newPiece
        return result

    def getHeight(self):
        """Returns the maximum height a column of placed blocks has reached"""
        currHeight = 0
        for r in range(len(self.board)-1, -1, -1):
            foundBlock = False
            for c in range(len(self.board[r])):
                if self.board[r][c] != 0:
                    foundBlock = True
                    currHeight += 1
                    break

            if foundBlock == False:
                break
        return currHeight

    def isTerminal(self):
        """determines if the tiles have reached the top of the game"""
        is_over = False
        for c in range(len(self.board[0])):
            if self.board[0][c] != 0:
                is_over = True
                break
        return is_over

    def setPiece(self, tetr):
        """Sets the Board's falling Tetromino to a given Tetromino"""
        self.fallingPiece = Tetromino(tetr.type)
        self.fallingPiece.setState(tetr.getState())

    def makePieceFall(self):
        """Pushes the piece completely down the board"""
        while not self.isPieceDoneFalling():
            self.fallingPiece.moveDown(1)
        self.fallingPiece.moveDown(-1)

    def getValidMoves(self):
        """Returns a list of tuple associations that correlate to the distance to cover
        and rotations to make to get the Tetromino to the corresponding state"""
        result = []
        initialBoard = self.makeCopy()
        rotationStates = []

        # see how many rotation states we have
        i = 0
        while i < 4 and initialBoard.fallingPiece.rotationState not in rotationStates:
            rotationStates.append(initialBoard.fallingPiece.rotationState)
            initialBoard.fallingPiece.rotate(1)

        for i in range(len(rotationStates)):
            moveDist = 0
            rotationBoard = self.makeCopy()

            # rotate fallingPieces to our current rotationState, our starting point
            while rotationBoard.fallingPiece.rotationState != rotationStates[i]:
                rotationBoard.fallingPiece.rotate(1)

            # move left/right until we can't
            moveRight = True
            moveLeft = True
            while moveLeft or moveRight:
                leftBoard = rotationBoard.makeCopy()
                rightBoard = rotationBoard.makeCopy()
                if moveLeft:
                    movePossible = leftBoard.fallingPiece.moveX(-moveDist)
                    leftBoard.makePieceFall()
                    if leftBoard.isPieceDoneFalling() or movePossible == False:
                        moveLeft = False
                    else:
                        leftBoard.makeMove()
                        result.append(((-moveDist, leftBoard.fallingPiece.rotationState), leftBoard.getState()))
                if moveRight:
                    movePossible = rightBoard.fallingPiece.moveX(moveDist)
                    rightBoard.makePieceFall()
                    if rightBoard.isPieceDoneFalling() or movePossible == False:
                        moveRight = False
                    elif moveDist != 0:
                        rightBoard.makeMove()
                        result.append(((moveDist, rightBoard.fallingPiece.rotationState), rightBoard.getState()))
                moveDist += 1

        return result

    def makeMove(self):
        """ updates board array with squares from fallen tetromino
        (only called when tetromino is done falling)"""
        for point in self.fallingPiece.getPoints():
            self.board[point[0]][point[1]] = 1

    def checkTetris(self):
        """check rows that are full (full rows called tetris)
         and remove them, return amount of rows removed """
        # delete full rows and add blank rows at top
        full_rows = []
        # get index of rows that are full
        for i in range(len(self.board)):
            is_cleared = True
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    is_cleared = False
                    continue
            if is_cleared:
                full_rows.append(i)

        # delete full rows and add an empty row at the top
        for i in range(len(full_rows)):
            self.board.pop(full_rows[i])
            for j in range(len(full_rows)):
                if i != j and full_rows[i] > full_rows[j]:
                    full_rows[j] += 1

            self.board.insert(0, [])
            for c in range(config['cols']):
                self.board[0].append(0)

        # return number of rows we deleted
        return len(full_rows)

    def rotatePiece(self):
        """Rotates the piece, with respect to the
        tetromino's type, only if allowable"""
        if self.fallingPiece.type == 2:
            return

        # get original state in case test cases don't work
        originalState = self.fallingPiece.getState()
        self.fallingPiece.rotate(1)
        tests = []

        # get tests cases for rotation correction
        if self.fallingPiece.type == 1:
            if self.fallingPiece.rotationState == 0:
                tests = [(-1, 0)]
            elif self.fallingPiece.rotationState == 1:
                tests = [(-1, 0), (0, 1)]
        else:
            if self.fallingPiece.rotationState == 1:
                tests = [(1, 0), (1, -1), (0, 2), (1, 2)]
            elif self.fallingPiece.rotationState == 3:
                tests = [(-1, 0), (-1, -1), (0, 2), (-1, 2)]

        # run through test cases for piece
        for testTuple in tests:
            if not (self.isPieceDoneFalling()):
                break
            self.fallingPiece.moveDown(-testTuple[1])
            self.fallingPiece.moveX(testTuple[0])

        # if no test cases work, undo rotation
        if self.isPieceDoneFalling():
            self.fallingPiece.setState(originalState)

    def isPieceDoneFalling(self):
        """determines if piece is at the bottom of its fall:
        Checks if board is out of bounds either left right or upwards
        then checks if piece is already in board, indicating that its fallen"""
        for point in self.fallingPiece.getPoints():
            if point[0] >= config['rows']:
                return True
            elif point[1] < 0 or point[1] >= config['cols']:
                return True
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] != 0:
                    for point in self.fallingPiece.getPoints():
                        if r == point[0] and c == point[1]:
                            return True
        return False

    def makeNewPiece(self):
        """Changes falling piece to a random configuration of one,
        using the bag to ensure that the piece types are cycling through"""
        if len(self.bag) == 0:
            self.bag = [1, 2, 3, 4, 5, 6, 7]
        randInt = random.choice(self.bag)
        self.bag.remove(randInt)
        self.fallingPiece = Tetromino(randInt)

    def print(self):
        """prints string representation of board"""
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                inPiece = False
                for point in self.fallingPiece.points:
                    if point[0] == r and point[1] == c:
                        print("-", end='')
                        inPiece = True
                        break
                if not inPiece:
                    print(self.board[r][c], end='')
            print()
