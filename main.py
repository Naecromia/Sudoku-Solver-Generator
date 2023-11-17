import random


class SudokuTile:
    def __init__(self, name='Default Square', size=3):
        self.possibilities = list(range(1, size**2 + 1))
        self.tileName = name
        self.value = 'X'

    def setValue(self, value):
        if self.value != 'X':
            return 2
        if value in self.possibilities or value == 'X':
            self.value = value
            return 1
        return 0

    def unsetValue(self):
        if self.value != 'X':
            self.value = 'X'
            return 1
        return 0

    def getValue(self):
        return self.value

    def getPossibilities(self):
        return self.possibilities

    def getName(self):
        return self.tileName

    def restrictValue(self, value):
        if value in self.possibilities:
            self.possibilities.remove(value)
            return 1
        return 0

    def unrestrictValue(self, value):
        if value not in self.possibilities:
            self.possibilities.append(value)
            return 1
        return 0

    def __str__(self):
        return f"{self.tileName}"

    def __repr__(self):
        return f"{self.tileName}: {self.value}"


class SudokuBoard:

    def __init__(self, size=3, startingDigits=0):
        self.board = []
        self.boardSize = size
        for x in range(size**2):
            row = []
            for y in range(size**2):
                row.append(SudokuTile('Tile' + str(x*size + y) + ' (' + str(x) + ',' + str(y) + ')', size))
            self.board.append(row)

        # TODO fix initial tile generation
        for _ in range(startingDigits):
            rowCoordinate = random.randint(0, len(self.board) - 1)
            colCoordinate = random.randint(0, len(self.board) - 1)
            tile = self.board[rowCoordinate][colCoordinate]
            while tile.getValue() != 'X':
                rowCoordinate = random.randint(0, len(self.board) - 1)
                colCoordinate = random.randint(0, len(self.board) - 1)
                tile = self.board[rowCoordinate][colCoordinate]
            tile.setValue(tile.getPossibilities()[random.randint(0, len(tile.getPossibilities()) - 1)])
            self.restrictTiles(rowCoordinate, colCoordinate, tile.getValue())

    def restrictTiles(self, row_index, col_index, value):
        # row:
        for tile in self.board[row_index]:
            tile.restrictValue(value)
        # col:
        for row in range(len(self.board)):
            self.board[row][col_index].restrictValue(value)
        # subsquare:
        subsquareRow = (row_index // self.boardSize) * self.boardSize
        subsquareCol = (col_index // self.boardSize) * self.boardSize
        for x in range(self.boardSize):
            for y in range(self.boardSize):
                self.board[subsquareRow + x][subsquareCol + y].restrictValue(value)

    def unrestrictTiles(self, row_index, col_index, value):
        # row:
        for tile in self.board[row_index]:
            tile.unrestrictValue(value)
        # col:
        for row in range(len(self.board)):
            self.board[row][col_index].unrestrictValue(value)
        # subsquare:
        subsquareRow = (row_index // self.boardSize) * self.boardSize
        subsquareCol = (col_index // self.boardSize) * self.boardSize
        for x in range(self.boardSize):
            for y in range(self.boardSize):
                self.board[subsquareRow + x][subsquareCol + y].unrestrictValue(value)

    def setTile(self, row_index, col_index, value):
        if row_index > len(self.board) or col_index > len(self.board):
            print(f'Invalid Unassignment: Tile index out of bounds.')
            return 0
        res = self.board[row_index][col_index].setValue(value)
        if res == 2:
            print(f'Invalid Assignment: Tile already set to value {self.board[row_index][col_index].getValue()}.')
            return 0
        elif res == 0:
            print(f'Invalid Assignment: Tile cannot be {value}.')
            return 0
        self.restrictTiles(row_index, col_index, value)
        return 1

    def unsetTile(self, row_index, col_index):
        if row_index > len(self.board) or col_index > len(self.board):
            print(f'Invalid Unassignment: Tile index out of bounds.')
            return
        initialVal = self.board[row_index][col_index].getValue()
        res = self.board[row_index][col_index].unsetValue()
        if res == 0:
            print(f'Invalid Unassignment: Tile does not have a value.')
            return
        self.unrestrictTiles(row_index, col_index, initialVal)

    def getPossibilities(self, row_index, col_index):
        if row_index >= len(self.board) or col_index >= len(self.board):
            print(f'Invalid Unassignment: Tile index out of bounds.')
            return
        print(f'{self.board[row_index][col_index].getName()} can be'
              f' {self.board[row_index][col_index].getPossibilities()}.')

    def isSolved(self):
        # check all tiles have values
        for row in self.board:
            for tile in row:
                if tile.getValue() == 'X':
                    return 0

        expectedNums = set(range(1, board.boardSize**2 + 1))

        # rows:
        for row in self.board:
            rowNums = []
            for tile in row:
                rowNums.append(tile.getValue())
            if set(rowNums) != expectedNums:
                return 0

        # cols:
        for row in range(len(self.board)):
            colNums = []
            for col in range(len(self.board)):
                colNums.append(self.board[row][col].getValue())
            if set(colNums) != expectedNums:
                return 0

        # subsquares:
        for subsquareRow in range(self.boardSize):
            for subsquareCol in range(self.boardSize):
                subsquareNums = []
                for x in range(self.boardSize):
                    for y in range(self.boardSize):
                        subsquareNums.append(self.board[subsquareRow*self.boardSize + x]
                                             [subsquareCol*self.boardSize + y].getValue())
                if set(subsquareNums) != expectedNums:
                    return 0
        return 1

    def solveBoard(self):
        priorityTile = None
        numPossibilities = -1
        tileCoordinates = (0, 0)
        for row_index in range(len(self.board)):
            # sort tiles to identify tile with fewest options
            # if any have 0 possibilities revert
            for tile_index in range(len(self.board[row_index])):
                tile = self.board[row_index][tile_index]
                if tile.getValue() == 'X':  # check if tile not assigned
                    if len(tile.getPossibilities()) == 0:
                        # no possible values for tile, cannot complete board
                        return 0
                    elif len(tile.getPossibilities()) == 1:
                        # only one possible value, test if valid
                        currVal = tile.getValue()
                        tile.setValue(tile.getPossibilities()[0])
                        self.restrictTiles(row_index, tile_index, tile.getValue())
                        if self.solveBoard() == 0:
                            # no possible value for tile
                            self.unrestrictTiles(row_index, tile_index, tile.getValue())
                            tile.setValue(currVal)
                            return 0
                        return 1
                    else:
                        # get a tile with fewest possibilities
                        if priorityTile is None:
                            priorityTile = tile
                            numPossibilities = len(tile.getPossibilities())
                            tileCoordinates = (row_index, tile_index)
                        elif numPossibilities > len(tile.getPossibilities()):
                            priorityTile = tile
                            numPossibilities = len(tile.getPossibilities())
                            tileCoordinates = (row_index, tile_index)

        if priorityTile is None:
            # no unassigned tiles remain, board must be complete
            return 1

        # test priority tile
        currVal = priorityTile.getValue()
        for possibleValue in priorityTile.getPossibilities():
            priorityTile.setValue(possibleValue)
            self.restrictTiles(tileCoordinates[0], tileCoordinates[1], priorityTile.getValue())
            if self.solveBoard() == 1:
                # valid assignment found
                return 1
            # assignment invalid, reset tile
            self.unrestrictTiles(tileCoordinates[0], tileCoordinates[1], priorityTile.getValue())
            priorityTile.setValue(currVal)
        # no possible assignment for tile, cannot complete board
        return 0

    def printBoard(self):
        returnStr = ''
        for row_index in range(len(self.board)):
            print('=' * ((self.boardSize ** 2) * 2 + self.boardSize) if row_index % self.boardSize == 0
                  else '-' * ((self.boardSize ** 2) * 2 + self.boardSize))
            print('|', end='')
            for tile_index in range(len(self.board[row_index])):
                print(str(self.board[row_index][tile_index].getValue()) + '|'
                      if self.board[row_index][tile_index].getValue() is not None else ' |',
                      end='' if tile_index != len(self.board[row_index]) - 1 else '\n')
                if (tile_index + 1) % self.boardSize == 0:
                    if tile_index != len(self.board[row_index]) - 1:
                        print('|', end='')
        print('=' * ((self.boardSize ** 2) * 2 + self.boardSize))

    def __str__(self):
        return 'Sudoku Board'


if __name__ == '__main__':
    repeat = 'y'
    print('--------Sudoku Solver---------')
    while repeat == 'y':
        print('Would you like to generate a board or input one yourself?')
        generateBoard = input('Enter \'y\' to input a board, or enter \'n\' to generate a random board: ')
        while generateBoard not in ['y', 'n']:
            print('Invalid Input: Please enter either \'y\' or \'n\'.')
            generateBoard = input('Enter \'y\' to input a board, or enter \'n\' to generate a random board: ')

        if generateBoard == 'y':
            print("What size Sudoku board would you like to input?")
            boardSize = input('Please input a size (for each subsquare) for the board: ')
            while not boardSize.isnumeric() or int(boardSize) <= 0:
                if not boardSize.isnumeric():
                    print('Invalid Input: Size must be an integer.')
                elif int(boardSize) <= 0:
                    print('Invalid Input: Size must be greater than 0.')
                boardSize = input('Please input a size for the board: ')

            boardSize = int(boardSize)
            board = SudokuBoard(boardSize)
            print('Next please input the digit for each tile going from left to right, top to bottom.\n'
                  'If the tile is empty please input \'x\'.\n'
                  'If there are no more digits to input please input \'done\'.')
            numInputted = 0
            while numInputted < boardSize:
                nextTile = input(f'Please input the digit for tile '
                                 f'({numInputted // boardSize},{numInputted % boardSize})')
                if nextTile.isnumeric():
                    if board.setTile(numInputted // boardSize, numInputted % boardSize, int(nextTile)):
                        numInputted += 1
                    else:
                        print(f'Error: Tile ({numInputted // boardSize},{numInputted % boardSize}) cannot be {nextTile}'
                              f'.\nPlease double check that you are submitting the board correctly.')
                elif nextTile == 'x':
                    numInputted += 1
                elif nextTile == 'done':
                    while numInputted < boardSize:
                        numInputted += 1
                else:
                    print('Invalid Input: Please submit a non-negative integer for the next tile,'
                          ' \'x\' if it is blank, or \'done\' if there are no more tiles to input.')
                    pass
                print('Current Board: ')
                board.printBoard()
        else:
            print("What size Sudoku would you like to generate?")
            boardSize = input('Please input a size (for each subsquare) for the board: ')
            while not boardSize.isnumeric() or int(boardSize) <= 0:
                if not boardSize.isnumeric():
                    print('Invalid Input: Size must be an integer.')
                elif int(boardSize) <= 0:
                    print('Invalid Input: Size must be greater than 0.')
                boardSize = input('Please input a size for the board: ')

            startingNums = input('How many starting digits should there be? ')
            while not startingNums.isnumeric() or int(startingNums) > int(boardSize)**4:
                if not startingNums.isnumeric():
                    print('Invalid Input: number of starting digits must be a positive integer')
                else:
                    print(f"Invalid Input: number of starting digits"
                          f" must not be greater than number of tiles({int(boardSize)**4})")
                startingNums = input('Please input a number of starting digits: ')

            board = SudokuBoard(int(boardSize), int(startingNums))
        print('Initial Board:')
        board.printBoard()
        print('Would you like to solve this board yourself or have an AI solve it?')
        autoSolve = input('Enter \'y\' to solve it yourself, or enter \'n\' to have the AI solve it: ')
        while autoSolve not in ['y', 'n']:
            print('Invalid Input: Please enter either \'y\' or \'n\'.')
            autoSolve = input('Enter \'y\' to have the AI solve it, or enter \'n\' to solve it yourself: ')

        if autoSolve == 'n':
            print('Solving Sudoku board...')
            if board.solveBoard() == 0:
                print('No valid solution to Sudoku board. Aborting.')
            else:
                print('Solving Sudoku board complete. This is the completed board:')
                board.printBoard()
        else:
            print('All tile coordinates start from (0,0).\n'
                  'Use \'set x y val\' or \'unset x y\' to change the value of the tile at (x,y).\n'
                  'Use \'possibilities x y\' to get the possible values of the tile at (x,y).\n'
                  'Type \'solve\' to solve the board.\n'
                  'Good luck!\n')
            userCommand = input('Please input your next step: ')
            while True:
                while True:
                    userCommand = userCommand.split(" ")
                    if userCommand[0] == 'set':
                        if len(userCommand) != 4:
                            print('Invalid Input. set command must be in the form of \'set x y value\'.')
                        elif not userCommand[1].isnumeric() or not userCommand[2].isnumeric():
                            print('Invalid Input. Coordinates must both be non-negative integers.')
                        else:
                            # handle set
                            board.setTile(int(userCommand[1]), int(userCommand[2]), int(userCommand[3]))
                            break
                    elif userCommand[0] == 'unset':
                        if len(userCommand) != 3:
                            print('Invalid Input. unset command must be in the form of \'unset x y\'.')
                        elif not userCommand[1].isnumeric() or not userCommand[2].isnumeric():
                            print('Invalid Input. Coordinates must both be non-negative integers.')
                        else:
                            # handle unset
                            board.unsetTile(int(userCommand[1]), int(userCommand[2]))
                            break
                    elif userCommand[0] == 'possibilities':
                        if len(userCommand) != 3:
                            print('Invalid Input. possibilities command must be in the form of \'possibilities x y\'.')
                        elif not userCommand[1].isnumeric() or not userCommand[2].isnumeric():
                            print('Invalid Input. Coordinates must both be non-negative integers.')
                        else:
                            # handle probabilities
                            board.getPossibilities(int(userCommand[1]), int(userCommand[2]))
                            break
                    elif userCommand[0] == 'solve':
                        if len(userCommand) != 1:
                            print('Invalid Input. solve command must be in the form of \'solve\'.')
                        else:
                            # handle solve
                            board.solveBoard()
                            break
                    else:
                        print('Invalid Input. Command must be one of set, unset, possibilities, or solve.')
                        userCommand = input('Please input your next step: ')

                print('New board state is: ')
                board.printBoard()
                if board.isSolved():
                    print('Board is solved!')
                    break
                userCommand = input('Please input your next step: ')

            print('Would you like to solve another Sudoku board?')
            repeat = input('Enter \'y\' if you would like to solve another board, or enter \'n\' to quit: ')
            while repeat not in ['y', 'n']:
                print('Invalid Input: Please enter either \'y\' or \'n\'.')
                repeat = input('Enter \'y\' if you would like to solve another board, or enter \'n\' to quit: ')
    print('Goodbye!')
