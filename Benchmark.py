from Player import *

class Benchmark:
    def __init__(self, player):
        self.running = True
        self.playerMoved = False
        self.mustMoveDown = True
        # initializing board
        self.board = Board()
        self.score = 0
        self.ticks = 0
        # initializing player
        self.player = player
        self.player.setBoard(self.board)
        self.player.moveLeft = self.moveLeft
        self.player.moveRight = self.moveRight
        self.player.moveRotate = self.moveRotate
        self.player.moveDown = self.moveDown
        self.player.update()

    def moveLeft(self):
        self.board.fallingPiece.moveX(-1)
        # prevents piece from moving through other pieces
        if self.board.isPieceDoneFalling():
            self.board.fallingPiece.moveX(1)
            self.playerMoved = True
    def moveRight(self):
        self.board.fallingPiece.moveX(1)
        # prevents piece from moving through other pieces
        if self.board.isPieceDoneFalling():
            self.board.fallingPiece.moveX(-1)
            self.playerMoved = True
    def moveDown(self):
        self.board.fallingPiece.moveDown(1)
        self.solidifyPieceIfNecessary()
        self.mustMoveDown = False
        self.playerMoved = True
    def moveRotate(self):
        self.board.rotatePiece()
        self.playerMoved = True

    def update(self):
        # is game over?
        if self.board.isTerminal():
            self.running = False

        self.player.update()

        self.ticks += 1
        if self.ticks < 1000 and not self.playerMoved:
            return
        # if fallingPiece is none, make a new falling piece
        if self.board.fallingPiece is None:
            self.board.makeNewPiece()
            self.playerMoved = False
        self.ticks = 0
        # add piece to board and if it did, check for cleared rows
        if self.mustMoveDown:
            self.board.fallingPiece.moveDown(1)
        else:
            self.mustMoveDown = True
        self.solidifyPieceIfNecessary()

    def solidifyPieceIfNecessary(self):
        """Given that the piece is done falling,
        moves the piece back up to no longer overlap with pre-placed,
        updates board with piece's squares, removes fallingPiece"""
        # solidifying piece
        if self.board.isPieceDoneFalling():
            self.board.fallingPiece.moveDown(-1)
            self.board.makeMove()
            self.board.fallingPiece = None
            # gotta do this
            self.checkAndRemoveTetris()

    def checkAndRemoveTetris(self):
        """uses checkTetris to remove the number of full rows
         and updates score based on number of removed rows"""
        numRows = self.board.checkTetris()
        if numRows == 1:
            self.score += 40
        elif numRows == 2:
            self.score += 100
        elif numRows == 3:
            self.score += 300
        elif numRows == 4:
            self.score += 1200

# main game loop
'''
totalScore = 0
maxScore = 0
minScore = 100000
numGames = 25
for i in range(numGames):
    bench = Benchmark(AIPlayer())

    while bench.running:
        bench.update()

    totalScore += bench.score
    if bench.score > maxScore:
        maxScore = bench.score
    if bench.score < minScore:
        minScore = bench.score
    print("score: "+str(bench.score))

print()
print("MAX SCORE: "+str(maxScore))
print("MIN SCORE: "+str(minScore))
print("AVERAGE SCORE: "+str(totalScore/numGames))
print("NUM GAMES: "+str(numGames))'''