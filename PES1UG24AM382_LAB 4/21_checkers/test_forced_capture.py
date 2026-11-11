
from board import move_piece
from rules import has_capture, capture_move, simple_move

board = [["."] * 8 for _ in range(8)]
board[4][1] = "R"
board[3][2] = "B"
board[5][4] = "R"

# Red has a legal capture from (4, 1) to (2, 3).
assert has_capture(board, "R")

# The capture must be recognized.
assert capture_move(board, "R", (4, 1), (2, 3))

# An ordinary move is geometrically possible,
# but should be prohibited by the game's forced-capture rule.
assert simple_move(board, "R", (5, 4), (4, 5))

print("PASS: Capture is available.")
print("PASS: Legal capture is recognized.")
print("PASS: Ordinary move is geometrically valid.")
print("NOTE: game.py must reject that ordinary move.")
