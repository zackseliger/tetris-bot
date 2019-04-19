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

class AIPlayer(Player):
    def __init__(self):
        super().__init__()

    def heuristic(self, board):
        # Initiate a high heuristic value
        heuristic_value = 10000000000
        # Terminated game is always the least competitive
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
                if current_space == 0:
                    # Check how many neighbor spaces are full
                    try:
                        if board_matrix[row+1][col] == 1:
                            neighbor_full_space += 1
                            top_full_space += 1
                    except:
                        IndexError
                    try:
                        if board_matrix[row-1][col] == 1:
                            neighbor_full_space += 1
                    except:
                        IndexError
                    try:
                        if board_matrix[row][col+1] == 1:
                            neighbor_full_space += 1
                    except:
                        IndexError
                    try:
                        if board_matrix[row][col-1] == 1:
                            neighbor_full_space += 1
                    except:
                        IndexError
                if top_full_space == 1:
                    if neighbor_full_space == 4:
                        heuristic_value -= 1500
                    # if neighbor_full_space == 3:
                    #     heuristic_value -= 100
                    # if neighbor_full_space == 2:
                    #     heuristic_value -= 80
                # if top_full_space == 0:
                #     heuristic_value -= 5000
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
        # the highest point is weighted really heavily since we want our ai to put Tetromino well-distributed.
        return heuristic_value - highest_point * 1000 - total_height * 400 - height_difference * 100

    def getMoves(self):
        if self.board.fallingPiece is None:
            return

        biggestHeuristic = 0
        biggestState = None
        validMoves = self.board.getValidMoves()
        for state in validMoves:
            hValue = self.heuristic(Board(state[1]))
            if hValue > biggestHeuristic:
                biggestHeuristic = hValue
                biggestState = state

        if biggestState is not None:
            for i in range(abs(biggestState[0][0])):
                if biggestState[0][0] > 0:
                    self.moveRight()
                if biggestState[0][0] < 0:
                    self.moveLeft()
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

class PaperPlayer(Player):

    def __init__(self):
        # initializes time, rotation
        time.clock()
        self.rotation = 1
        self.maxTime = 1000
        # replace 1000 with max time in milliseconds each miniMax call has to finish

    def heuristic(self, board):
        """copy the boardState and recursively call itself over each iteration of
        possible moves to that state
        doesn't alter board at all, used in future simulations
            -> passes board as arg"""
        heuristic_value = 0
        # If the board is terminal, give a large heuristic value
        # to represent that there is no game board worse
        if board.isTerminal:
            return 1000000000
        # Check whether there is a row that is already full and ready
        # to be cleared out. If yes, increment heuristic value.
        for row in range(len(board.board)):
            for col in range(len(board.board[row])):
                if board.board[row][col] == 0:
                    break
                if board.board[row][col] == 1 and col == len(board.board[row]) - 1:
                    heuristic_value += 0.3
                continue
        # Check whether there is any hole or gap in any row, If yes, increment heuristic value.
        for row in range(len(board.board)):
            heuristic_value += math.pow(self.heuristic_one_row(board, row, heuristic_value), (1/4.384))
        return heuristic_value

    def heuristic_one_row(self, board, row, heuVal):
        """doesn't alter board at all, used in future simulations
            -> passes board as arg"""
        # This helper function uses a loop to update the heuristic value based on any dependent row above the hole.
        # Recommend: add a helper function in board.py to get the highest point in this game.
        if not board.board:
            return 0
        for col in range(len(board.board[row])):
            if row + 3 >= len(board.board[row]) - 1:
                if board.board[row][col] == 0 and board.board[row + 1][col] == 1 and board.board[row+2][col]== 1\
                        and board.board[row+3][col] == 1:
                    heuVal += 17.72
                    heuVal += self.heuristic_one_row(board, row+1, heuVal + 1.16)
            if col >= 2 and col <= len(board.board[row]) - 4:
                if board.board[row][col] == board.board[row][col+1] and board.board[row][col] == 0:
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 2] == 0 and board.board[row + 1][col + 3] == 0:
                        heuVal += 1.63
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 2] == 1 and board.board[row + 2][col + 2] == 0\
                            and board.board[row + 1][col + 3] == 0:
                        heuVal += 2.15
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 2] == 0 and board.board[row + 2][col + 2] == 0\
                            and board.board[row + 1][col + 3] == 0:
                        heuVal += 2.15
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 2] == 0 and board.board[row + 1][col + 3] == 1:
                        heuVal += 1.31
                    if board.board[row + 1][col - 2] == 1 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 2] == 0 and board.board[row + 1][col + 3] == 0:
                        heuVal += 1.31
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 2] == 0 and board.board[row + 2][col -1] == 1\
                            and board.board[row + 1][col + 3] == 0:
                        heuVal += 1.79
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 2] == 1 and board.board[row + 2][col + 2] == 1\
                            and board.board[row + 1][col + 3] == 0:
                        heuVal += 1.79
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 2] == 1 and board.board[row + 1][col + 3] == 0:
                        heuVal += 2.72
                    if board.board[row + 1][col - 2] == 1 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 2] == 1 and board.board[row + 1][col + 3] == 0:
                        heuVal += 2.74
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 2] == 0 and board.board[row + 1][col + 3] == 1:
                        heuVal += 2.74
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 2] == 1 and board.board[row + 2][col - 1] == 1\
                            and board.board[row + 1][col + 3] == 0:
                        heuVal += 2.18
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 2] == 1 and board.board[row + 2][col + 2] == 1\
                            and board.board[row + 1][col + 3] == 0:
                        heuVal += 2.18
                    if board.board[row + 1][col - 2] == 1 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 2] == 0 and board.board[row + 1][col + 3] == 1:
                        heuVal += 1.77
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 2] == 0 and board.board[row + 2][col - 1] == 1\
                            and board.board[row + 1][col + 3] == 1:
                        heuVal += 2.09
                    if board.board[row + 1][col - 2] == 1 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 2] == 1 and board.board[row + 2][col + 2] == 1\
                            and board.board[row + 1][col + 3] == 0:
                        heuVal += 2.09
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 2][col - 1] == 1\
                            and board.board[row + 1][col + 2] == 1 and board.board[row + 2][col + 2] == 1\
                            and board.board[row + 1][col + 3] == 0:
                        heuVal += 5.48


                if not board[row][col] == board.board[row][col+1] and board[row][col] == 0:
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 1][col + 2] == 0:
                        heuVal += 1.55
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col + 1] == 0\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 2.01
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 2][col + 1] == 0\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 2.01
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 1][col + 2] == 1:
                        heuVal += 1.34
                    if board.board[row + 1][col - 2] == 1 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 1][col + 2] == 0:
                        heuVal += 1.34
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 2][col -1] == 1\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 2.57
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col + 1] == 1\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 2.57
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 1][col + 2] == 0:
                        heuVal += 2.69
                    if board.board[row + 1][col - 2] == 1 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 1][col + 2] == 0:
                        heuVal += 2.01
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 1][col + 2] == 1:
                        heuVal += 2.01
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col - 1] == 1\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 4.38
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col + 1] == 1\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 4.38
                    if board.board[row + 1][col - 2] == 1 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 1][col + 2] == 1:
                        heuVal += 1.55
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 2][col - 1] == 1\
                            and board.board[row + 1][col + 2] == 1:
                        heuVal += 2.55
                    if board.board[row + 1][col - 2] == 1 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col + 1] == 1\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 2.55
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 2][col - 1] == 1\
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col + 1] == 1\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 15
            if col == 1:
                if board.board[row][col] == board.board[row][col+1] and board.board[row][col] == 0:
                    if board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 2] == 0 and board.board[row + 1][col + 3] == 0:
                        heuVal += 1.63
                    if board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 2] == 1 and board.board[row + 2][col + 2] == 0\
                            and board.board[row + 1][col + 3] == 0:
                        heuVal += 2.15
                    if board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 2] == 0 and board.board[row + 2][col + 2] == 0\
                            and board.board[row + 1][col + 3] == 0:
                        heuVal += 2.15
                    if board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 2] == 0 and board.board[row + 1][col + 3] == 1:
                        heuVal += 1.31
                    if board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 2] == 0 and board.board[row + 2][col -1] == 1\
                            and board.board[row + 1][col + 3] == 0:
                        heuVal += 1.79
                    if board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 2] == 1 and board.board[row + 2][col + 2] == 1\
                            and board.board[row + 1][col + 3] == 0:
                        heuVal += 1.79
                    if board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 2] == 1 and board.board[row + 1][col + 3] == 0:
                        heuVal += 2.72
                    if board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 2] == 0 and board.board[row + 1][col + 3] == 1:
                        heuVal += 2.74
                    if board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 2] == 1 and board.board[row + 2][col - 1] == 1\
                            and board.board[row + 1][col + 3] == 0:
                        heuVal += 2.18
                    if board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 2] == 1 and board.board[row + 2][col + 2] == 1\
                            and board.board[row + 1][col + 3] == 0:
                        heuVal += 2.18
                    if board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 2][col - 1] == 1\
                            and board.board[row + 1][col + 2] == 1 and board.board[row + 2][col + 2] == 1\
                            and board.board[row + 1][col + 3] == 0:
                        heuVal += 5.48


                if not board[row][col] == board.board[row][col+1] and board[row][col] == 0:
                    if board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 1][col + 2] == 0:
                        heuVal += 1.55
                    if board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col + 1] == 0\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 2.01
                    if board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 2][col + 1] == 0\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 2.01
                    if board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 1][col + 2] == 1:
                        heuVal += 1.34
                    if board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 2][col -1] == 1\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 2.57
                    if board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col + 1] == 1\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 2.57
                    if board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 1][col + 2] == 0:
                        heuVal += 2.69
                    if board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 1][col + 2] == 1:
                        heuVal += 2.01
                    if board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col - 1] == 1\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 4.38
                    if board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col + 1] == 1\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 4.38
                    if board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 2][col - 1] == 1\
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col + 1] == 1\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 15
            if col == 0:
                if board.board[row][col] == board.board[row][col+1] and board.board[row][col] == 0:
                    if board.board[row + 1][col + 2] == 0 and board.board[row + 1][col + 3] == 0:
                        heuVal += 1.79
                    if board.board[row + 1][col + 2] == 1 and board.board[row + 2][col + 2] == 0\
                            and board.board[row + 1][col + 3] == 0:
                        heuVal += 2.18
                    if board.board[row + 1][col + 2] == 0 and board.board[row + 1][col + 3] == 1:
                        heuVal += 2.09
                    if board.board[row + 1][col + 2] == 1 and board.board[row + 2][col + 2] == 1\
                            and board.board[row + 1][col + 3] == 0:
                        heuVal += 5.48

                if not board[row][col] == board.board[row][col+1] and board[row][col] == 0:
                    if board.board[row + 1][col + 1] == 0 and board.board[row + 1][col + 2] == 0:
                        heuVal += 2.57
                    if board.board[row + 1][col + 1] == 1 and board.board[row + 2][col + 1] == 0\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 4.38
                    if board.board[row + 1][col + 1] == 0 and board.board[row + 1][col + 2] == 1:
                        heuVal += 2.55
                    if board.board[row + 1][col + 1] == 1 and board.board[row + 2][col + 1] == 1\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 15

            if col == len(board.board[row]) - 1:
                if board[row+1][col-2] == 0 and board[row+1][col-1] == 0:
                    heuVal += 2.57
                if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1:
                    heuVal += 4.38
                if board.board[row + 1][col - 2] == 1 and board.board[row + 1][col - 1] == 0 \
                        and board.board[row + 1][col + 1] == 0 and board.board[row + 1][col + 2] == 0:
                    heuVal += 2.55
                if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                        and board.board[row + 1][col + 1] == 0 and board.board[row + 2][col - 1] == 1 \
                        and board.board[row + 1][col + 2] == 0:
                    heuVal += 15
            if col == len(board.board[row]) - 2:
                if board.board[row][col] == board.board[row][col+1] and board.board[row][col] == 0:
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 0:
                        heuVal += 1.55
                if not board[row][col] == board.board[row][col+1] and board[row][col] == 0:
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 0:
                        heuVal += 1.55
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col + 1] == 0:
                        heuVal += 2.01
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 2][col + 1] == 0:
                        heuVal += 2.01
                    if board.board[row + 1][col - 2] == 1 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 0:
                        heuVal += 1.34
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 2][col -1] == 1:
                        heuVal += 2.57
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col + 1] == 1:
                        heuVal += 2.57
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 1:
                        heuVal += 2.69
                    if board.board[row + 1][col - 2] == 1 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 1:
                        heuVal += 2.01
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col - 1] == 1:
                        heuVal += 4.38
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col + 1] == 1:
                        heuVal += 4.38
                    if board.board[row + 1][col - 2] == 1 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col + 1] == 1:
                        heuVal += 2.55
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 2][col - 1] == 1\
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col + 1] == 1:
                        heuVal += 15
            if col == len(board.board[row]) - 3:
                if board.board[row][col] == board.board[row][col+1] and board.board[row][col] == 0:
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 1.63
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 2] == 1 and board.board[row + 2][col + 2] == 0:
                        heuVal += 2.15
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 2] == 0 and board.board[row + 2][col + 2] == 0:
                        heuVal += 2.15
                    if board.board[row + 1][col - 2] == 1 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 1.31
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 2] == 0 and board.board[row + 2][col -1] == 1:
                        heuVal += 1.79
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 2] == 1 and board.board[row + 2][col + 2] == 1:
                        heuVal += 1.79
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 2] == 1:
                        heuVal += 2.72
                    if board.board[row + 1][col - 2] == 1 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 2] == 1:
                        heuVal += 2.74
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 2] == 1 and board.board[row + 2][col - 1] == 1:
                        heuVal += 2.18
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 2] == 1 and board.board[row + 2][col + 2] == 1:
                        heuVal += 2.18
                    if board.board[row + 1][col - 2] == 1 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 2] == 1 and board.board[row + 2][col + 2] == 1:
                        heuVal += 2.09
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 2][col - 1] == 1\
                            and board.board[row + 1][col + 2] == 1 and board.board[row + 2][col + 2] == 1:
                        heuVal += 5.48


                if not board[row][col] == board.board[row][col+1] and board[row][col] == 0:
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 1][col + 2] == 0:
                        heuVal += 1.55
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col + 1] == 0\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 2.01
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 2][col + 1] == 0\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 2.01
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 1][col + 2] == 1:
                        heuVal += 1.34
                    if board.board[row + 1][col - 2] == 1 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 1][col + 2] == 0:
                        heuVal += 1.34
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 2][col -1] == 1\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 2.57
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col + 1] == 1\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 2.57
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 1][col + 2] == 0:
                        heuVal += 2.69
                    if board.board[row + 1][col - 2] == 1 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 1][col + 2] == 0:
                        heuVal += 2.01
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 1][col + 2] == 1:
                        heuVal += 2.01
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col - 1] == 1\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 4.38
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col + 1] == 1\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 4.38
                    if board.board[row + 1][col - 2] == 1 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 1][col + 2] == 1:
                        heuVal += 1.55
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 1][col + 1] == 0 and board.board[row + 2][col - 1] == 1\
                            and board.board[row + 1][col + 2] == 1:
                        heuVal += 2.55
                    if board.board[row + 1][col - 2] == 1 and board.board[row + 1][col - 1] == 0 \
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col + 1] == 1\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 2.55
                    if board.board[row + 1][col - 2] == 0 and board.board[row + 1][col - 1] == 1 \
                            and board.board[row + 2][col - 1] == 1\
                            and board.board[row + 1][col + 1] == 1 and board.board[row + 2][col + 1] == 1\
                            and board.board[row + 1][col + 2] == 0:
                        heuVal += 15
        return heuVal

    def getValidMoves(self):
        return ("LEFT","RIGHT","DOWN","ROTATE", "NONE")

    def getChild(self, move):
        newBoard = Board(self.board.getState())
        newPiece = self.board.fallingPiece
        if move == "LEFT":
            newBoard.makeFallingPiece(newPiece.moveX(-1))
        if move == "RIGHT":
            newBoard.makeFallingPiece(newPiece.moveX(1))
        if move == "DOWN":
            newBoard.makeFallingPiece(newPiece.moveDown)
        if move == "ROTATE":
            newBoard.makeFallingPiece(newPiece.rotate(1))
        #while not newBoard.isPieceDoneFalling():
        #    newBoard.makeFallingPiece(newPiece.moveDown)
        #newBoard.makeMove()
        return newBoard

    def minimax(self, depth, board):
        """Depth is the amount of time remaining, uses self.board"""
        # minimax copied from my a5-player - cited Lecture 11 PDF
        term = board.isTerminal()
        bestMove = None
        # id terminal positions and assign them constant w/o unneccesasary processing
        if term:
            return None, 10000000000
        # stop at max depth and return approp heuristic val
        if not term and depth <= 0:
            return None, self.heuristic(board)
        bestVal = math.inf
        # getValidMoves returns list of Boards after placement of piece
        # heuristic
        for col in board.getValidMoves():
            val = self.minimax(self.board.getChild(col), depth - 1)[1]
            if self.board.turn == 1:
                if val < bestVal:
                    bestMove = col
                    bestVal = val
        # returns the best move and best score as a tuple
        return bestMove, bestVal

    def getMoves(self):
        """calls minimax, sets time constaint in milliseconds"""
        move, score = self.minimax(self.board, self.maxTime - pygame.time.get_ticks())
        # checking keys and possibly sending events
        if move == "LEFT":
            self.moveLeft()
        if move == "RIGHT":
            self.moveRight()
        if move == "DOWN":
            self.moveDown()
        if move == "ROTATE":
            self.moveRotate()