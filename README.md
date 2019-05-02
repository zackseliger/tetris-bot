# tetris
Final project for CSCI-B351

There are three artificial intelligence players: YifanPlayer, ZackPlayer, DrewPlayer

To play the game: run the Window class, using the keyboard responsive HumanPlayer()
  left to move piece left, right to move piece right, down to push piece down, up to rotate
To run tests: run the Benchmark class, using any artificial intelligence player
  To alter the number of tests or the player being tested: go to the marked lines within Benchmark
** if using one of the three artificial players, running Window or Benchmark will throw
    an error every time a piece lands because it is updating the heuristic in between
    landing the piece and getting the next piece. Does not affect gameplay**
To alter the board size configurations: use the Settings.py class
  This class also holds shortcuts for userEvents and their Types

The piece falling down is called a Tetromino, a filled row is called a Tetris
Board.py holds a copy of a piece, a matrix of filled coordinate positions, and a bag of possible types to cycle through.
  -can return the max height of filled pieces, a copy of itself, a list of valid moves to make
  -can rotate, make a singular move or even completely push down their piece, check whether its reached the bottom
  -can check whether a row should be cleared, whether the filled pieces have reached the top
Player.py is a superclass which contains getMoves(which each subclass overrides), an update function for 
  the thread, and the moves: right, left, down, and rotate. 
  -Each subclass overrides their getMoves to use the various moves.
Window.py has a board, piece and uses them to run the game
  -can represent board and piece on pygame, checks and removes full rows, solidifies pieces when done falling, 
  -updates taking into consideration other thread, pygame events
