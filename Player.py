# Player class for Tetris
import threading
from Settings import *
import time

class Player:
    def __init__(self):
        self.thread = threading.Thread(target=(self.getMoves))

    def getMoves(self):
        pass

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
            self.thread = threading.Thread(target=(self.getMoves))
            self.thread.start()


class HumanPlayer(Player):
    def getMoves(self):
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
# if human player, connect moves to keyboard events
# if not, connect moves to highest heuristic score
    def __init__(self):
        # should initialize time
        time.clock()
        # should initialize PlayerType [I, L, S, O(cube)]
        # all subsequent calls to time.clock() will return
        # float rep. of seconds since this call
        # current rotation: 1-4
        self.rotation = 1
        # if rotation is > 4, reset to 1


    #comparisons to a4-Player
        # rather than returning negative for 2nd player good positions,
            # return negative for positions that increases likelihood of failure
                #maybe represented as costs of clearance or closeness to top
        # minimax_ab and minimax both seemed useful so I added them and combind findMove
        # NOTE: caching previous heuristics would cut down on runtime as the game goes on
    def heuristic(self, board):
        """copy the boardState and recursively call itself over each iteration of
        possible moves to that state"""
        #notes from heuristic design paper
        # they used a dampening function to reduce the importance
            # of rows with high cost to clear (I piece horizontal)
        heuristic_value = 0
        #If the board is terminal, give a large heuristic value in order to represent that there is no game board worse
        #than this board.
        if board.isTerminal:
            return 1000000000
        #Check whether there is a row that is already full and ready to be cleared out. If yes, increment heuristic
        #value.
        for row in range(len(board.board)):
            for col in range(len(board.board[row])):
                if board.board[row][col] == 0:
                    break
                if board.board[row][col] == 1 and col == len(board.board[row])- 1:
                    heuristic_value += 0.3
                continue
        #Check whether there is any hole or gap in any row, If yes, increment heuristic value.
        for row in range(len(board.board)):
            heuristic_value += Math.pow(self.heuristic_one_row(board, row, heuristic_value), (1/4.384))
        return heuristic_value

    # This helper function uses a loop to update the heuristic value based on any dependent row above the hole.
    # Recommend: add a helper function in board.py to get the highest point in this game.
    def heuristic_one_row(self, board, row, heuVal):
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

    def getInput(self):
        """check keyboard input for human player"""
    def drawPlayer(self):
        """Represents player as 2d array signifying shape or however is best for
            pygame"""
        # extra comments are rotations of each original configuration
        if self.playerType == "I":
            grid = {(1,1,1,1,1)}
            #grid = {(1,0,0,0,0)
            #        (1,0,0,0,0)
            #        (1,0,0,0,0)
            #        (1,0,0,0,0)
            #        (1,0,0,0,0)}
        elif self.playerType == "S":
            grid = {(1,1,0,0,0)
                    (0,1,1,0,0)}
            #grid = {(0,1,1,0,0)
            #        (1,1,0,0,0)}
            #grid = {(0,1,0,0,0)
            #        (1,1,0,0,0)
            #        (1,0,0,0,0)}
            #grid = {(1,0,0,0,0)
            #        (1,1,0,0,0)
            #        (0,1,0,0,0)}
        elif self.playerType == "cube":
            grid = {(1,1,0,0,0)
                    (1,1,0,0,0)}
        elif self.playerType = "L":
            grid = {(1,1,1,1,0)
                    (1,0,0,0,0)}
            #grid = {(0,0,0,1,0)
            #        (1,1,1,1,0)}
            #grid = {(1,0,0,0,0)
            #        (1,0,0,0,0)
            #        (1,0,0,0,0)
            #        (1,1,0,0,0)}
            #grid = {(0,1,0,0,0)
            #        (0,1,0,0,0)
            #        (0,1,0,0,0)
            #        (1,1,0,0,0)}

    # minimax copied from my a5-player
    # super easy to adjust for tetris
    def minimax(self, board, depth):
        # cited Lecture 11 PDF
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
        if board.turn == 1:
            bestVal = math.inf
        else:
            bestVal = -math.inf
        for col in board.getValidMoves():
            val = self.minimax(board.getChild(col), depth - 1)[1]
            if board.turn == 1:
                if val < bestVal:
                    bestMove = col
                    bestVal = val
            else:
                if val > bestVal:
                    bestMove = col
                    bestVal = val
        # returns the best move and best score as a tuple
        return bestMove, bestVal

    # minimax_ab copied from my a5-player
    def minimax_ab(self, board, depth, alpha, beta):
        # cited Lecture 12 Games III PDF
        # return null move and appropriate score constant
        term = board.isTerminal()
        if term == 0:
            return None, self.P1_WIN_SCORE
        move = None
        if term == -1:
            return None, self.DRAW_SCORE
        if term == 1:
            return None, self.P2_WIN_SCORE
        if term is None and depth <= 0:
            return None, self.heuristic(board)

        bestvalue = None
        for col in board.getValidMoves():
            m, value = self.minimax_ab(board.getChild(col), depth - 1, alpha, beta)
            if board.turn == 1:
                if move is None or value < bestvalue:
                    bestvalue = value
                    move = col
                    # beta  represents the score of min's current strategy
                    beta = min(beta, value)
                    if alpha >= beta:
                # in a cutoff situation, return the score that resulted in the cutoff
                       break
            if board.turn == 0:
                if move is None or value > bestvalue:
                    bestvalue = value
                    move = col
                    # alpha represents the score of max's current strategy
                    alpha = max(value, alpha)
                    if beta <= alpha:
                # in a cutoff situation, return the score that resulted in the cutoff
                        break
        # returns the best move and best score as a tuple
        return move, bestvalue

    def findMove(self, board):
        #move, score = self.minimax(board, self.depthLimit)
        #move, score = self.minimax_ab(board, self.depthLimit, -math.inf, math.inf)
        return move
