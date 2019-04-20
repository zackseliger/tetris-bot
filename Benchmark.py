from Player import *

class Benchmark:
    def __init__(self, player):
        self.running = True
        self.playerMoved = False
        self.mustMoveDown = True
        self.startTime = time.time()
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
    def moveRight(self):
        self.board.fallingPiece.moveX(1)
        # prevents piece from moving through other pieces
        if self.board.isPieceDoneFalling():
            self.board.fallingPiece.moveX(-1)
    def moveDown(self):
        self.board.fallingPiece.moveDown(1)
        self.solidifyPieceIfNecessary()
        self.mustMoveDown = False
    def moveRotate(self):
        self.board.rotatePiece()

    def update(self):
        time.sleep(0.02)
        # is game over?
        if self.board.isTerminal():
            self.running = False

        if self.player.thread.is_alive() == False:
            self.playerMoved = True
        self.player.update()

        if time.time()-self.startTime < 0.02 and not self.playerMoved:
            return
        self.startTime = time.time()

        # if fallingPiece is none, make a new falling piece
        if self.board.fallingPiece is None:
            self.board.makeNewPiece()
            self.playerMoved = False

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
totalScore = 0
maxScore = 0
minScore = 100000
numGames = 50
start = time.time()
for i in range(numGames):
    bench = Benchmark(ZackPlayer())

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
print("NUM GAMES: "+str(numGames))
print("TIME ELAPSED: "+str(time.time()-start))
print("AVG TIME PER GAME: "+str((time.time()-start)/numGames))