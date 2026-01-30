import enum


class GridPosition(enum.Enum):
    EMPTY = 0
    YELLOW = 1
    RED = 2


class Grid:
    def __init__(self, rows, columns):
        self._rows = rows
        self._columns = columns
        self._grid = None
        self.initGrid()

    def initGrid(self):
        self._grid = [
            [GridPosition.EMPTY for _ in range(self._columns)]
            for _ in range(self._rows)
        ]

    def getGrid(self):
        return self._grid

    def getColumnCount(self):
        return self._columns

    def placePiece(self, column, piece):
        if column < 0 or column >= self._columns:
            raise ValueError("Invalid column")
        if piece == GridPOsition.EMPTY:
            raise ValueError("Invalid piece")
        for row in range(self._rows - 1, -1, -1):
            if self._grid[row][column] == GridPosition.EMPTY:
                self._grid[row][column] = piece
                return row

    def checkWin(self, connectN, row, col, piece):
        count = 0
        for c in range(self._columns):
            if self._grid[row][c] == piece:
                count += 1
            else:
                count = 0
