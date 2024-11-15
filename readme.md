## Compiling and Running

build with AI model with `make -f twency48/build/makefile`

from root (twenty48AI) directory

select mode by changing which function is commented out in the main function of main.py.

Run with `python3 main.py`.


## Dependencies

`pip install twenty48`

This is a package I made that contains the base game, with a flexible interface for changing the display and inputs [twenty48](https://github.com/KyleJMcMaster/twenty48/blob/main/src/twenty48/Board.py)


If running on windows, recompile the c agent as a .dll and modify the code in `MarkovDPAI.py` in class `Expectimax7` or `Expectimax8`

## Extra info

The algorithm is a standard expectiminimax, which enumerates all of the states to a certain depth. At this depth, the score for each state is estimated using a heuristic function. The function works by taking the current score and subtracting a penalty based on the position of the tiles. The penalty encourages states which have the largest tile in the bottom right corner, and the remaining tiles to follow a montonic 'snake' pattern down the rest of the board. The penalty parameters were selected using bayesian optimization (SOBOL + GPEI).
