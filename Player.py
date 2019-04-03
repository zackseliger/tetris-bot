# Player class for Tetris
import time
class Player:
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
    def heuristic(self, boardState):
        """copy the boardState and recursively call itself over each iteration of
        possible moves to that state"""
        #notes from heuristic design paper
        # they used a dampening function to reduce the importance
            # of rows with high cost to clear (I piece horizontal)
        
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
