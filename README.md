# Sudoku-Solver-Generator
A program that allows for the generation of sudoku boards with custom sizes and difficulties, and utilizes an AI to solve generated boards or user inputted boards.

# Generating A Board:
For generating a board input the size of one subsquare. For refence, a regular Sudoku board has subsquares of size 3. 
Next input the number of tiles that should be revealed to begin with. This must be at least 0 and no more than the number of tiles in the board.

# Inputting A Board:
First set up the board's size the same way as generating the board, then input the board's initial state.
To input the board's initial state you must input each tile's value individually, using 'x' for a blank tile. This goes from left to right, top to bottom.
You can input 'done' once all remaining tiles are blank tiles to leave the remaining tiles as blank.

# User Board Solving:
When solving a board yourself use the following commands:
'\set x y val' - Sets the tile at (x,y) to have the value val. 
'\unset x y' - Sets the tile at (x,y) to be blank.
'\possibilities x y' - Prints the list of values the tile at (x,y) can be.
'\solve' - Uses an AI to attempt solve the board from the current state.

Each command will tell you if the command was successful, or if there was an issue performing the command. For example, using an invalid tile coordinate or setting a tile to a value it cannot be will print the relevant issue.
Tile coordinates start at (0,0) in the top left.
