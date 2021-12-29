from random import shuffle
from enum import Enum

class Minesweeper:
    class GameState(str, Enum):
        PLAYING = 'Playing'
        WIN = 'Win'
        LOSE = 'Lose'


    class CellContent(Enum):
        UNKNOWN = -1
        EMPTY = 0
        MINE = 9

    class CellPrintChar(str, Enum):
        UNKNOWN = '?'
        EMPTY = '-'
        MINE = 'X'


    def __init__(self, width=10, height=10, mine_count=10):
        # Check there are not more mines than cells
        if mine_count > width * height:
            raise ValueError('There can not be more mines than cells \
                (got %d mines and %d total cells)' % mine_count, width * height)

        # Store variables
        self.width = width
        self.height = height
        self.mine_count = mine_count
        self.cell_count = width * height
        self.hidden_cells = self.cell_count
        self.game_state = Minesweeper.GameState.PLAYING

        # Create mine field
        base_cells = [True] * self.mine_count + \
            [False] * (self.cell_count - self.mine_count)
        shuffle(base_cells)

        # Create 2D lists
        self.cells_mines = [base_cells[i*self.height:(i+1)*self.height] \
            for i in range(self.width)]
        self.cells_neighboring = Minesweeper.convolve(self.cells_mines)
        self.cells_revealed = [[False] * height for _ in range(width)]


    def convolve(cells):
        # Initialize output grid
        width = len(cells)
        height = len(cells[0])
        output_grid = [[0] * height for _ in range(width)]

        # Perform convolution
        for x in range(width):
            for y in range(height):
                sum = 0

                for i in range(3):
                    if 0 <= x-i < width:
                        for j in range(3):
                            if 0 <= y-j < height:
                                sum += cells[x-i][y-j]

                output_grid[x][y] = sum

        # Return
        return output_grid


    def print_internal_state(self):
        print('=====')
        print('Width: %3d \tHeight: %3d \tMines %3d' % \
            (self.width, self.height, self.mine_count))
        print('State: %s' % repr(self.game_state.value))
        print('-----')
        for x in range(self.width):
            line = ''.join(Minesweeper.CellPrintChar.MINE.value \
                if self.cells_mines[x][i] \
                else Minesweeper.CellPrintChar.EMPTY.value \
                for i in range(self.height))
            print('\t' + line)
        print('=====')
