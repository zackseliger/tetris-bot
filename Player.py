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

    def minimax(self, depth, board):
        """Depth is the amount of time remaining, uses self.board"""
        # minimax copied from my a5-player - cited Lecture 11 PDF
        term = board.isTerminal()
        bestMove = None
        # id terminal positions and assign them constant w/o unneccesasary processing
        if term == -1:
            return None, self.DRAW_SCORE
        if term == 0:
            return None, self.P1_WIN_SCORE
        if term == 1:
            return None, self.P2_WIN_SCORE
        # stop at max depth and return approp heuristic val
        if not term and depth <= 0:
            return None, self.heuristic(board)
        bestVal = math.inf
        for col in board.getValidMoves():
            val = self.minimax(self.board.getChild(col), depth - 1)[1]
            if self.board.turn == 1:
                if val < bestVal:
                    bestMove = col
                    bestVal = val
        # returns the best move and best score as a tuple
        return bestMove, bestVal

    def findMove(self):
        """calls minimax, sets time constaint in milliseconds"""
        move, score = self.minimax(self.board, self.maxTime - pygame.time.get_ticks())
        return move
