import random


def generate_board(width):
    board = list(range(1, width ** 2)) + [0]  # 1-8 numbers and 0 as the empty space

    # Loops to shuffle the board until it is solvable but not already solved
    while True:
        random.shuffle(board)
        if is_solvable(board) and not is_solved(board, width):
            return board


def is_solvable(board):
    """Uses inversion (i appears before j, but i > j) to determine if it is solvable"""
    board_width = int(len(board) ** (1 / 2))   # Calculate the width (e.g., 4x4)
    inversions = 0

    # Loop through every value in the board
    for i in range(len(board)):
        # Loop through every value in the board after i to compare to
        for j in range((i + 1), len(board)):
            # Determine if it is an inversion (i > j), skipping the empty tile
            if board[i] != 0 and board[j] != 0 and board[i] > board[j]:
                inversions += 1

    if board_width % 2 == 1:
        # Odd width is solvable if inversions are even (width - 1)
        return inversions % 2 == 0
    else:
        # Even width needs to consider the empty space's row (count from bottom to up)
        empty_row_from_bottom = board_width - (board.index(0) // board_width)
        return (inversions + empty_row_from_bottom) % 2 == 1


def is_solved(board, width):
    return board == list(range(1, width ** 2)) + [0]


def can_move(board, tile):
    empty_index = board.index(0)
    tile_index = board.index(tile)
    width = int(len(board) ** 0.5)  # Dynamically calculate the board's width

    # Calculate row and column positions for the empty space and the tile
    empty_row, empty_col = divmod(empty_index, width)
    tile_row, tile_col = divmod(tile_index, width)

    # Check if the tile is adjacent to the empty space (either horizontally or vertically)
    return (abs(empty_row - tile_row) == 1 and empty_col == tile_col) or \
           (abs(empty_col - tile_col) == 1 and empty_row == tile_row)


def move_tile(board, tile):
    empty_index = board.index(0)
    tile_index = board.index(tile)

    # positional swap for tile and empty space
    board[empty_index], board[tile_index] = board[tile_index], board[empty_index]

