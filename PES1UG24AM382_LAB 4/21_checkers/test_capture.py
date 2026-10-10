
from board import move_piece
from rules import capture_move

# Create an empty 8x8 board.
board = [["."] * 8 for _ in range(8)]

# Set up a capture position.
board[4][3] = "R"  # Red piece
board[3][4] = "B"  # Black piece

print("Board before capture:")
for row in board:
    print(" ".join(row))

# Test whether the capture is legal.
assert capture_move(board, "R", (4, 3), (2, 5)), (
    "FAIL: A valid capture was rejected."
)

# Perform the capture.
move_piece(board, (4, 3), (2, 5))

print("\nBoard after capture:")
for row in board:
    print(" ".join(row))

# Verify the result.
assert board[2][5] == "R", "FAIL: Red did not reach the destination."
assert board[4][3] == ".", "FAIL: Starting square was not cleared."
assert board[3][4] == ".", "FAIL: Captured Black piece was not removed."

print("\nPASS: Capture validation works.")
print("PASS: Captured piece was removed.")
print("PASS: Red reached the destination.")
print("PASS: Starting square was cleared.")
