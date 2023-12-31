"""
Sudoku solver from Bard.google.com, ref github.com/AMiragaia/UA [404] and
https://www.kosbie.net/cmu/summer-12/15-112/handouts/hw6.html [CMU 15-112
Summer 2012 Homework 6].

This program uses the backtracking algorithm to solve Sudoku puzzles. The
backtracking algorithm works by first trying all possible solutions for a given
cell. If no solution is found, the algorithm backtracks and tries a different
solution for the cell. This process continues until a solution is found or all
possible solutions have been tried.

The time complexity of this program is O(9!), which is the number of possible
Sudoku puzzles. The space complexity of this program is O(9^2), which is the
space required to store the board."""

# timeit.timeit('solve_sudoku(BOARD2)', globals=globals(), number=1000)
# On 2018 MBP:
#   Original list of list of int representation:   42 - 45 sec (42-45 msec/run)
#   List of array of byte representation:          53 - 56 sec
#   List of list; avoid repeat work in is_valid():      30 sec
#   [Similarly avoiding repeat work in solve_sudoku_helper() only helped ≈3%.]
#   numpy array of int8:                          742 sec [10 * number=100]
#   numpy array of int32:                         733 sec [10 * number=100]

# timeit.timeit('solve_sudoku(BOARD2)', globals=globals(), number=1000)
# On 2018 MBP:
#   List of list; avoid rework in is_valid():     211 sec

# Idea: For hard cases, it might save time to set cells with only one
# possibility (one pencil mark) before a backtracking pass.

BOARD1 = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]]

BOARD2 = [  # "Annoying" level
    [3, 0, 0, 5, 8, 0, 0, 6, 0],
    [4, 0, 0, 0, 0, 0, 2, 0, 3],
    [0, 9, 0, 0, 2, 0, 0, 5, 0],
    [0, 5, 0, 0, 4, 0, 0, 0, 8],
    [0, 0, 0, 7, 0, 1, 0, 0, 0],
    [7, 0, 0, 0, 9, 0, 0, 4, 0],
    [0, 3, 0, 0, 7, 0, 0, 2, 0],
    [8, 0, 6, 0, 0, 0, 0, 0, 9],
    [0, 4, 0, 0, 3, 8, 0, 0, 7]]

BOARD3 = [  # "Maelstrom" level
    [7, 0, 0, 0, 8, 0, 4, 0, 1],
    [4, 0, 8, 0, 0, 3, 0, 0, 0],
    [0, 5, 0, 4, 0, 0, 3, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 9],
    [0, 0, 7, 0, 3, 0, 1, 0, 0],
    [1, 0, 0, 0, 4, 0, 0, 0, 0],
    [0, 0, 4, 0, 0, 1, 0, 2, 0],
    [0, 0, 0, 5, 0, 0, 7, 0, 4],
    [2, 0, 6, 0, 9, 0, 0, 0, 5]]


def solve_sudoku(initial_board: list[list[int]]):
    """
    Solves a Sudoku puzzle.

    Args:
      initial_board: A 9x9 array representing the Sudoku puzzle. Each cell
        contains 0 for unknown or 1 - 9.

    Returns:
      A solved Sudoku puzzle.
    """

    def is_valid(board: list[list[int]], row: int, col: int, num: int):
        """
        Checks if the given number is valid at the given row and column in the
        board.

        Args:
          board: A 9x9 array representing the Sudoku puzzle.
          row: The row index.
          col: The column index.
          num: The number to check.

        Returns:
          True if the number is valid, False otherwise.
        """

        # Check the row.
        for cell in board[row]:
            if cell == num:
                return False

        # Check the column.
        for board_row in board:
            if board_row[col] == num:
                return False

        # Check the 3x3 block.
        row_start = row // 3 * 3
        col_start = col // 3 * 3
        for board_row in board[row_start:row_start + 3]:
            for cell in board_row[col_start:col_start + 3]:
                if cell == num:
                    return False

        return True

    def solve_sudoku_helper(board: list[list[int]]):
        """
        Recursive helper function to solve the Sudoku puzzle.

        Args:
          board: A 9x9 array representing the Sudoku puzzle.

        Returns:
          True if the puzzle is solved, False otherwise.
        """

        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    # Try each number from 1 to 9.
                    for num in range(1, 10):
                        if is_valid(board, row, col, num):
                            board[row][col] = num

                            # Recursively solve the rest of the puzzle.
                            if solve_sudoku_helper(board):
                                return True

                    # If none of the numbers work, the puzzle is unsolvable.
                    board[row][col] = 0
                    return False

        return True

    # Make a working copy.
    board = [row.copy() for row in initial_board]

    # Solve the puzzle.
    solve_sudoku_helper(board)

    return board


def test_solver():
    expected2 = [
        [3, 2, 7, 5, 8, 4, 9, 6, 1],
        [4, 6, 5, 9, 1, 7, 2, 8, 3],
        [1, 9, 8, 3, 2, 6, 7, 5, 4],
        [6, 5, 9, 2, 4, 3, 1, 7, 8],
        [2, 8, 4, 7, 6, 1, 3, 9, 5],
        [7, 1, 3, 8, 9, 5, 6, 4, 2],
        [5, 3, 1, 4, 7, 9, 8, 2, 6],
        [8, 7, 6, 1, 5, 2, 4, 3, 9],
        [9, 4, 2, 6, 3, 8, 5, 1, 7],
    ]
    solution = solve_sudoku(BOARD2)
    assert solution == expected2
