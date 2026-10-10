
from rules import simple_move, capture_move, has_capture
from board import move_piece

# Create an empty board.
board = [["."] * 8 for _ in range(8)]

# Set up Red and Black pieces.
board[4][1] = "R"
board[3][2] = "B"

# Red has a capture available from (4, 1) to (2, 3).
assert has_capture(board, "R"), "FAIL: Capture was not detected."

assert capture_move(board, "R", (4, 1), (2, 3)), (
    "FAIL: Legal capture was rejected."
)

# Verify that an ordinary move is geometrically valid.
board2 = [["."] * 8 for _ in range(8)]
board2[5][0] = "R"

assert simple_move(board2, "R", (5, 0), (4, 1)), (
    "FAIL: Ordinary move was rejected."
)

# Perform the capture and verify the result.
move_piece(board, (4, 1), (2, 3))

assert board[2][3] == "R"
assert board[3][2] == "."
assert board[4][1] == "."

print("PASS: Capture availability detected.")
print("PASS: Legal capture accepted.")
print("PASS: Ordinary move validated.")
print("PASS: Captured piece removed.")
