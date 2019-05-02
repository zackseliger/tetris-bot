# Player class for Tetris
import threading
from Settings import *
import time
from Board import *
import math


class Player:
    def __init__(self):
        self.thread = threading.Thread(target= self.getMoves)
        self.board = Board()

    def getMoves(self):
        pass

    def setBoard(self, board):
        self.board = board

    # the explicit definitions for sending events
    def moveLeft(self):
        pygame.event.post(userEvents['left'])

    def moveRight(self):
        pygame.event.post(userEvents['right'])

    def moveDown(self):
        pygame.event.post(userEvents['down'])

    def moveRotate(self):
        pygame.event.post(userEvents['rotate'])

    def update(self):
        if self.thread.is_alive() == False:
            self.thread = threading.Thread(target=self.getMoves)
            self.thread.start()


class HumanPlayer(Player):

    def getMoves(self):
        """Overrides parent function of same name
        to ask user for moves"""
        time.sleep(0.1)  # so that keyboard inputs aren't recognized too quickly

        # checking keys and possibly sending events
        keys = pygame.key.get_pressed()  # checking pressed keys
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.moveLeft()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.moveRight()
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.moveDown()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.moveRotate()

class ZackPlayer(Player):
    def __init__(self):
        super().__init__()
        self.goalState = None
        self.savedStates = {}

    def heuristic(self, board):
        result = 0
        boardState = board.getState()

        # see if we saved this value before (dynamic programming)
        if boardState in self.savedStates:
            return self.savedStates[boardState]

        # bad if this board is already game over
        if board.isTerminal():
            return -100000

        # modify copy of board to not have full rows
        filledRows = board.checkTetris()
        result += 50*filledRows

        # check for holes
        for r in range(len(board.board)-1, -1, -1):
            for c in range(len(board.board[r])):
                if board.board[r][c] == 0:
                    if r != 0 and board.board[r - 1][c] != 0:
                        result -= 50

        # find highest height
        maxHeight = 0
        for c in range(len(board.board[0])):
            numSquares = 0
            for r in range(len(board.board)-1, -1, -1):
                if board.board[r][c] != 0:
                    numSquares += 1
            if numSquares > maxHeight:
                maxHeight = numSquares
        # subtract diff in heights from every column
        for c in range(len(board.board[0])):
            numSquares = 0
            for r in range(len(board.board) - 1, -1, -1):
                if board.board[r][c] != 0:
                    numSquares += 1
            result -= (maxHeight - numSquares) * 2

        # save result into dictionary
        self.savedStates[boardState] = result

        # return final heuristic
        return result

    def getMoves(self):
        if self.board.fallingPiece is None:
            self.goalState = None
            return

        biggestHeuristic = -100000000
        biggestState = None
        validMoves = self.board.getValidMoves()
        for state in validMoves:
            hValue = self.heuristic(Board(state[1]))
            if hValue > biggestHeuristic:
                biggestHeuristic = hValue
                biggestState = state

        if biggestState is not None and self.goalState != biggestState[1]:
            a = self.board.fallingPiece.rotationState
            while a != biggestState[0][1]:
                self.moveRotate()
                a += 1
                if a > 3:
                    a = 0
                if self.board.fallingPiece.type == 1 and a > 1:
                    a = 0
                if self.board.fallingPiece.type == 2:
                    a = 0
            for i in range(abs(biggestState[0][0])):
                if biggestState[0][0] > 0:
                    self.moveRight()
                if biggestState[0][0] < 0:
                    self.moveLeft()
            self.goalState = biggestState[1]

        return biggestState[0]

class YifanPlayer(Player):
    def __init__(self):
        super().__init__()
        self.goalState = None

    def heuristic(self, board):
        # Initiate a high heuristic value
        heuristic_value = 10000000000
        # Update the board and clear out those rows that are completely filled
        board.checkTetris()
        # Terminated game is always the least competitive
        if board.isTerminal():
            return 0
        # Setting up some variables that will be used in calculation
        # trace the height difference from each column
        height_difference = 0
        # trace the total height of the game
        total_height = 0
        # mark the column already seen.
        marked = dict()
        # Get the board
        board_matrix = board.board
        # Double nested loop that goes through each space
        for row in range(board.size[0]):
            for col in range(board.size[1]):
                current_space = board_matrix[row][col]
                # Those spaces that are filled with an empty space which is at least one column below them will
                # reduce the heuristic significantly since those empty spaces are considered as holes that cannot reach
                # easily.
                bot_empty_space = 0
                if current_space == 1:
                    # Check how many spaces below that are empty
                    try:
                        if board_matrix[row + 1][col] == 0:
                            for i in range(board.size[0] - row):
                                if board_matrix[row + i][col] == 0:
                                    bot_empty_space += 1
                    except:
                        IndexError
                # Punish those boards with one space filled above and at least one spaces below that are empty with
                # lower heuristic values
                if bot_empty_space >= 1:
                    heuristic_value -= 1000000 * bot_empty_space
                if bot_empty_space == 0:
                    heuristic_value += 1
                # if current space is filled
                if current_space == 1:
                    # always gets the highest point in a column
                    if not col in marked.keys():
                        current_height = board.size[0] - row
                        total_height += current_height
                        marked[col] = current_height
        # Calculate the height difference since we want our ai to put Tetromino well-distributed.
        for i in range(board.size[1]):
            current_col = marked.get(i)
            prev_col = marked.get(i - 1)
            if not i == 0 and current_col and prev_col:
                height_difference += abs(current_col - prev_col)
            if not i == 0 and not current_col and prev_col:
                height_difference += prev_col
            if not i == 0 and current_col and not prev_col:
                height_difference += current_col
        # the highest point is weighted really heavily since we want our ai to put Tetromino well-distributed.
        return heuristic_value - total_height * 297 - height_difference * 97

    def getMoves(self):
        if self.board.fallingPiece is None:
            self.goalState = None
            return

        biggestHeuristic = 0
        biggestState = None
        validMoves = self.board.getValidMoves()
        for state in validMoves:
            hValue = self.heuristic(Board(state[1]))
            if hValue > biggestHeuristic:
                biggestHeuristic = hValue
                biggestState = state

        if biggestState is not None and self.goalState != biggestState[1]:
            a = self.board.fallingPiece.rotationState
            while a != biggestState[0][1]:
                self.moveRotate()
                a += 1
                if a > 3:
                    a = 0
                if self.board.fallingPiece.type == 1 and a > 1:
                    a = 0
                if self.board.fallingPiece.type == 2:
                    a = 0
            for i in range(abs(biggestState[0][0])):
                if biggestState[0][0] > 0:
                    self.moveRight()
                if biggestState[0][0] < 0:
                    self.moveLeft()
            self.goalState = biggestState[1]

    
class DrewPlayer(Player):
    def __init__(self):
        super().__init__()
        self.goalState = None
        self.savedStates = {}

    def heuristic(self, board):
        # start at bottom len(board.board) - 1, go up
        if board.isTerminal():
            return 0
        height = board.getHeight()
        hVal = height
        for row in range(len(board.board) - 1, height - 1, -1):
            for col in range(len(board.board[row])):
                if board.board[row][col] == 0:
                    if board.board[row-1][col] == 0:
                        try:
                            if board.board[row][col+1] == 0:
                                if board.board[row][col-1] == 0:
                                    hVal += 300
                        except IndexError:
                            pass
                    else:
                        hVal -= 100
                else:
                    hVal += 1

        self.savedStates[board.getState()] = hVal
        return hVal

    def getMoves(self):
        if self.board.fallingPiece is None:
            self.goalState = None
            return

        biggestHeuristic = -100000000
        biggestState = None
        validMoves = self.board.getValidMoves()
        for state in validMoves:
            hValue = self.heuristic(Board(state[1]))
            if hValue > biggestHeuristic:
                biggestHeuristic = hValue
                biggestState = state

        if biggestState is not None and self.goalState != biggestState[1]:
            a = self.board.fallingPiece.rotationState
            while a != biggestState[0][1]:
                self.moveRotate()
                a += 1
                if a > 3:
                    a = 0
                if self.board.fallingPiece.type == 1 and a > 1:
                    a = 0
                if self.board.fallingPiece.type == 2:
                    a = 0
            for i in range(abs(biggestState[0][0])):
                if biggestState[0][0] > 0:
                    self.moveRight()
                if biggestState[0][0] < 0:
                    self.moveLeft()
            self.goalState = biggestState[1]