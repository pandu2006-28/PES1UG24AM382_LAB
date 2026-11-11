
from board import move_piece
from rules import capture_move, has_capture, promote, simple_move

# Test 1: A regular piece can capture forward.
board = [["."] * 8 for _ in range(8)]
board[4][1] = "R"
board[3][2] = "B"

assert capture_move(board, "R", (4, 1), (2, 3))
move_piece(board, (4, 1), (2, 3))
assert board[3][2] == "."
assert board[2][3] == "R"
print("PASS: Regular capture works.")

# Test 2: A second capture is available.
board = [["."] * 8 for _ in range(8)]
board[4][1] = "R"
board[3][2] = "B"
board[1][4] = "B"

move_piece(board, (4, 1), (2, 3))
assert has_capture(board, "R", (2, 3))
assert capture_move(board, "R", (2, 3), (0, 5))
print("PASS: Follow-up capture detected.")

# Test 3: A Red king can move backward.
board = [["."] * 8 for _ in range(8)]
board[3][2] = "RK"
assert simple_move(board, "R", (3, 2), (4, 3))
print("PASS: King can move backward.")

# Test 4: Promotion at the back row.
board = [["."] * 8 for _ in range(8)]
board[0][1] = "R"
board[7][0] = "B"

promote(board)
assert board[0][1] == "RK"
assert board[7][0] == "BK"
print("PASS: Promotion works.")
