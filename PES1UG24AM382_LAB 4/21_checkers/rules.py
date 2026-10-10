
SIZE = 8


def simple_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    piece = board[sr][sc]

    if piece not in (player, player + "K"):
        return False

    if not (0 <= er < SIZE and 0 <= ec < SIZE):
        return False

    if board[er][ec] != ".":
        return False

    if abs(er - sr) != 1 or abs(ec - sc) != 1:
        return False

    direction = -1 if player == "R" else 1

    # Kings may move forward or backward.
    if piece.endswith("K"):
        return True

    return er - sr == direction


def capture_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    piece = board[sr][sc]

    if piece not in (player, player + "K"):
        return False

    if not (0 <= er < SIZE and 0 <= ec < SIZE):
        return False

    if board[er][ec] != ".":
        return False

    if abs(er - sr) != 2 or abs(ec - sc) != 2:
        return False

    direction = -1 if player == "R" else 1

    # Regular pieces capture forward only.
    # Kings capture in either direction.
    if not piece.endswith("K") and er - sr != 2 * direction:
        return False

    mr = (sr + er) // 2
    mc = (sc + ec) // 2
    middle = board[mr][mc]

    return middle not in (".", player, player + "K")


def promote(board):
    for c in range(SIZE):
        if board[0][c] == "R":
            board[0][c] = "RK"

        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"


def has_pieces(board, player):
    return any(
        piece in (player, player + "K")
        for row in board
        for piece in row
    )


def has_capture(board, player, position=None):
    """Check whether a player, or one specified piece, can capture."""
    for r in range(SIZE):
        for c in range(SIZE):
            if position is not None and (r, c) != position:
                continue

            piece = board[r][c]
            if piece not in (player, player + "K"):
                continue

            directions = (-1, 1) if piece.endswith("K") else (
                (-1,) if player == "R" else (1,)
            )

            for dr in directions:
                for dc in (-1, 1):
                    end = (r + 2 * dr, c + 2 * dc)

                    if (
                        0 <= end[0] < SIZE
                        and 0 <= end[1] < SIZE
                        and capture_move(board, player, (r, c), end)
                    ):
                        return True

    return False


def has_legal_move(board, player):
    """Check whether a player has at least one legal move."""
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] not in (player, player + "K"):
                continue

            for dr in (-1, 1):
                for dc in (-1, 1):
                    end = (r + dr, c + dc)
                    if (
                        0 <= end[0] < SIZE
                        and 0 <= end[1] < SIZE
                        and simple_move(board, player, (r, c), end)
                    ):
                        return True

                    end = (r + 2 * dr, c + 2 * dc)
                    if (
                        0 <= end[0] < SIZE
                        and 0 <= end[1] < SIZE
                        and capture_move(board, player, (r, c), end)
                    ):
                        return True

    return False
