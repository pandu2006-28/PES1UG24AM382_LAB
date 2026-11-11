
SIZE = 8


def initial_board():
    board = [["."] * SIZE for _ in range(SIZE)]

    # Place Black pieces in the first three rows.
    for r in range(3):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "B"

    # Place Red pieces in the last three rows.
    for r in range(5, 8):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "R"

    return board


def move_piece(board, start, end):
    sr, sc = start
    er, ec = end

    piece = board[sr][sc]

    # Remove the jumped piece during a capture.
    if abs(er - sr) == 2 and abs(ec - sc) == 2:
        mr = (sr + er) // 2
        mc = (sc + ec) // 2
        board[mr][mc] = "."

    # Move the piece.
    board[er][ec] = piece
    board[sr][sc] = "."
