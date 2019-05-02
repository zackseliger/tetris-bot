# Tetris
Final project for CSCI-B351.

### Prerequisites
Pygame is needed to run our project. You can install it with 'pip install pygame'

### How to run
We have two parts to our project - a live game and a benchmarking toolset. The game resides in Window.py, and the benchmarks lie in Benchmark.py. Run the file that you want to.

### Adjusting Parameters
In Window.py, the constructor for Window takes a Player parameter, as does the Benchmark class in Benchmark.py. We have 4 players:
* HumanPlayer - you can play the game! Only used for debug, and as such, we didn't polish. Input feels really clunky.
* ZackPlayer - The Player that Zack made (named Zackie). Has the lowest average score and is the slowest.
* DrewPlayer - The Player that Andrew made (named Brock). Has a fair average score and is the fastest.
* YifanPlayer - The Player that Yifan made (named Numera). Has the highest average score (by a wide margin) and is fairly quick.

Additionally, you may want to adjust the amount of games that Benchmark.py runs. It can be near the bottom of the file, in a variable called `numGames`.