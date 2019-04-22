# Player class for Tetris
import threading
from settings import *
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

        # number of blocks on filled rows + first non-filled row
        for r in range(len(board.board)-1, -1, -1):
            fullRow = True
            for c in range(len(board.board[r])):
                if board.board[r][c] == 0:
                    if r != 0 and board.board[r-1][c] != 0:
                        result -= 110
                        pass
                    fullRow = False
            if fullRow:
                result += 50

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
            result -= (maxHeight - numSquares) * 5
        #result -= board.getHeight() * 10

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
        # Terminated game is always the least competitive
        board.checkTetris()
        if board.isTerminal():
            return 0
        # Setting up some variables that will be used in calculation
        # trace the highest point in the game
        highest_point = -1
        # trace the height difference from each column
        height_difference = 0
        # trace the total height of the game
        total_height = 0
        # mark the column already seen.
        marked = dict()
        board_matrix = board.board
        for row in range(board.size[0]):
            for col in range(board.size[1]):
                current_space = board_matrix[row][col]
                neighbor_full_space = 0
                top_full_space = 0
                if current_space == 1:
                    # Check how many neighbor spaces are full
                    try:
                        if board_matrix[row+1][col] == 0:
                            neighbor_full_space += 1
                            for i in range(board.size[0] - row):
                                top_full_space += 1
                    except:
                        IndexError
                    try:
                        if board_matrix[row-1][col] == 0:
                            neighbor_full_space += 1
                    except:
                        IndexError
                    try:
                        if board_matrix[row][col+1] == 0:
                            neighbor_full_space += 1
                    except:
                        IndexError
                    try:
                        if board_matrix[row][col-1] == 0:
                            neighbor_full_space += 1
                    except:
                        IndexError
                if top_full_space == 1:
                    heuristic_value -= 10000
                    # if col > 0 and col < board.size[1] - 1 and row > 0 and row < board.size[0] - 1:
                    #     if neighbor_full_space == 4:
                    #         heuristic_value -= 16000
                    #     if neighbor_full_space == 3:
                    #         heuristic_value -= 600
                    #     if neighbor_full_space == 2:
                    #         heuristic_value -= 200
                    # else:
                    #     if col == 0 and row == 0 \
                    #             or col == 0 and row == board.size[0] - 1 \
                    #             or col == board.size[1] - 1 and row == 0\
                    #             or col == board.size[1] - 1 and row == board.size[0] - 1:
                    #         if neighbor_full_space == 2:
                    #             heuristic_value -= 1800
                    #         if neighbor_full_space == 1:
                    #             heuristic_value -= 400
                    #     else:
                    #         if neighbor_full_space == 3:
                    #             heuristic_value -= 1700
                    #         if neighbor_full_space == 2:
                    #             heuristic_value -= 700
                    #         if neighbor_full_space == 1:
                    #             heuristic_value -= 300
                if top_full_space == 0:
                    heuristic_value += 1
                # if current space is filled
                if current_space == 1:
                    # always gets the highest point in a column
                    if not col in marked.keys():
                        total_height += board.size[0] - row
                        marked[col] = board.size[0] - row
                    # update the highest point
                    if board.size[0] - row > highest_point:
                        highest_point = board.size[0] - row
        # Calculate the height difference since we want our ai to put Tetromino well-distributed.
        for i in range(board.size[1]):
            if not i == 0 and marked.get(i) and marked.get(i-1):
                height_difference += abs(marked[i] - marked[i - 1])
            if not i == 0 and not marked.get(i) and marked.get(i-1):
                height_difference += 20
            if not i == 0 and marked.get(i) and not marked.get(i-1):
                height_difference += 20
        # the highest point is weighted really heavily since we want our ai to put Tetromino well-distributed.
        return heuristic_value - highest_point * 173 - total_height * 397 - height_difference * 97

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