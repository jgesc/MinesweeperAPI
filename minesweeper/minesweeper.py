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
        self.cells_revealed = [[False] * height for _ in range(width)]
        self.cells_neighboring = [
            [
                sum([self.cells_mines[x][y] for x, y in self.neighbors(x, y)])
                for y in range(height)
            ]
            for x in range(width)
        ]


    def neighbors(self, x, y):
        for i in range(3):
            if 0 <= x-i < self.width:
                for j in range(3):
                    if 0 <= y-j < self.height:
                        yield (x-i, y-j)


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


    def get_visible_cells(self):
        return \
        [
            [
                self.cells_neighboring[x][y] if self.cells_revealed[x][y]
                else Minesweeper.CellContent.UNKNOWN
                for y in range(self.height)
            ]
            for x in range(self.width)
        ]


    def floodfill_empty(self, initial):
        pending = {initial}

        # While pending cells
        while pending:
            # Pop cell
            x, y = pending.pop()
            # Set to revealed
            self.cells_revealed[x][y] = True
            # Add neighbors to pending set
            pending |= {
                (x, y) for x, y in self.neighbors(x, y) if \
                self.cells_neighboring[x][y] == Minesweeper.CellContent.EMPTY \
                and not self.cells_revealed[x][y] \
            }
