
from rules import has_pieces, has_legal_move

# Test a player who has no pieces.
board = [["."] * 8 for _ in range(8)]
board[3][2] = "R"

assert has_pieces(board, "R")
assert not has_pieces(board, "B")
assert has_legal_move(board, "R")

# Test a Red piece blocked by Black pieces.
blocked = [["."] * 8 for _ in range(8)]
blocked[0][1] = "R"
blocked[1][0] = "B"
blocked[1][2] = "B"

assert not has_legal_move(blocked, "R")

print("PASS: remaining pieces detected.")
print("PASS: no-pieces condition detected.")
print("PASS: no-legal-moves condition detected.")
