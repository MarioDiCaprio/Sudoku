import random
from typing import List, Tuple, Union
import numpy


class Sudoku:
    """
    This class represents a sudoku game. It takes a 9x9 matrix as input
    in order to properly represent the game. It is possible to generate
    new sudoku automatically, as well as solving given sudoku.
    """

    def __init__(self, matrix: List[List[int]] = None):
        """
        Builds a Sudoku. By default, a new sudoku is generated
        if a matrix is not specified. Note that it needs to be a
        9x9 matrix.
        :param matrix: A 9x9 matrix that represents the sudoku
        """
        self.matrix = matrix

        # default: generated sudoku
        if self.matrix is None:
            self.generate()

    def __str__(self) -> str:
        """
        Returns this sudoku as a string
        :return: The sudoku as a string
        """
        return numpy.asarray(self.matrix).__str__()

    def in_row(self, num: int, col: int) -> bool:
        """
        Checks whether the given number is in the row of the
        given column
        :param col: The column
        :param num: The number
        :return: Whether the given number is in the row of the given column
        """
        return num in [arr[col] for arr in self.matrix]

    def in_col(self, num: int, row: int) -> bool:
        """
        Checks whether the given number is in the column of the
        given row
        :param row: The row
        :param num: The number
        :return: Whether the given number is in the column of the given row
        """
        return num in self.matrix[row]

    def in_box(self, num: int, position: Tuple[int, int]) -> bool:
        """
        Checks whether the given number is in the 3x3 box of the given
        position
        :param num: The number
        :param position: The position
        :return: Whether the given number is in the 3x3 box of the given position
        """
        y, x = position
        for i in range(3):
            for j in range(3):
                modY = y % 3
                modX = x % 3
                if self.matrix[y + i - modY][x + j - modX] == num:
                    return True
        return False

    def solve(self) -> Union[List[List[int]], None]:
        """
        Solves this sudoku. This is a backtracking algorithm.
        The solution is returned as a result. Note that 'self.matrix'
        is changed accordingly.
        :return: The solved matrix on success, 'None' on failure
        """
        # index of next empty square
        x, y = -1, -1

        # find index of next empty square
        for i in range(9):
            for j in range(9):

                # if square is empty: set index to that position
                if self.matrix[i][j] == 0:
                    x, y = j, i

        # if no space left (i.e. sudoku is solved): return current matrix
        if x == -1 and y == -1:
            return self.matrix

        # loop through all possible numbers (1-9) and try as solution
        for num in range(1, 10):
            # used to check if a number is legal
            col = self.in_col(num, y)
            row = self.in_row(num, x)
            box = self.in_box(num, (y, x))

            # if illegal number: skip this number
            if col or row or box:
                continue

            # insert number and try to solve recursively
            self.matrix[y][x] = num
            solved = self.solve()

            # if solution failed: try with another number
            if solved is None:
                self.matrix[y][x] = 0
            # else: return solution
            else:
                return solved

        # if all solutions failed: return 'None'
        return None

    def generate(self, clues: int = 30):
        """
        Generates a new sudoku and assigns it to 'self.matrix'.
        :param clues: Number of initial clues
        """
        # generate a matrix of 0's
        # last row are numbers from 1-9, shuffled
        tmp = list(range(1, 10))
        random.shuffle(tmp)
        self.matrix = [[0 for _ in range(9)] for _ in range(9)]
        self.matrix[8] = tmp

        # solve this matrix to fill the rest of the sudoku totaling 81 squares
        self.solve()

        # list all positions to exclude
        positions = [(i, j) for i in range(9) for j in range(9)]
        excludes = []
        while len(excludes) <= (81 - clues):

            # shuffle positions while first index is already excluded
            random.shuffle(positions)
            while positions[0] in excludes:
                random.shuffle(positions)

            excludes.append(positions[0])

        # delete all excluded positions from matrix
        for p in excludes:
            i, j = p
            self.matrix[i][j] = 0

    def clear(self):
        """
        Clears the whole matrix. All elements are set to 0.
        """
        self.matrix = [[0 for _ in range(9)] for _ in range(9)]
