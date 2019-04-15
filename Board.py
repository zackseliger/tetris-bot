# Board for Tetris
from Settings import config

class Board:
    def __init__(self, state=None):
        self.board = []
        self.size = config["rows"], config["cols"]
        for r in range(self.size[0]):
            self.board.append([])
            for c in range(self.size[1]):
                self.board[r].append(0)
        if state is not None:
            # state is string rep filled squares
            for i in range(len(state)):
                # row = i / size[0], col = i % size[1]
                if state[i] == "1":
                    self.board[(i / self.size[0])][(i % self.size[1])] = 1

    def get_board(self):
        return self.board

    def get_state(self):
        """converts board to a string"""
        state = ""
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                state += self.board[row][col]
        return state

    def is_terminal(self):
        """determines if the tiles have reached the top of the game"""
        is_over = False
        for c in range(len(self.board[0])):
            if self.board[0][c] != 0:
                is_over = True
                break
        return is_over

    def make_move(self, piece):
        """ given a tetromino, update points in board"""
        for point in piece.getPoints():
            self.board[point[0]][point[1]] = 1

    def check_tetris(self):
        """check rows that are full and remove them, return amount of rows removed """
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

    def is_piece_done_falling(self, tetromino):
        """determines if piece is at the bottom of its fall"""
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
# board calls getMove by Player: returns LEFT RIGHT DOWN ROTATE NOMOVE
    # player has a way of determining which move to make
        # human players key input
# updates board
