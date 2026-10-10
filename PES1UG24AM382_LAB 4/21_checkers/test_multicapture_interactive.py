from unittest.mock import patch
from game import Checkers

game = Checkers()
game.board = [["."] * 8 for _ in range(8)]

# Set up a two-capture sequence for Red.
game.board[4][1] = "R"
game.board[3][2] = "B"
game.board[1][4] = "B"

# Another Red piece tests whether the same piece must continue.
game.board[5][0] = "R"

inputs = [
    "4 1 2 3",  # First capture
    "5 0 4 1",  # Try moving a different Red piece
    "2 3 0 5",  # Second capture and promotion
    "q",
]

with patch("builtins.input", side_effect=inputs):
    with patch("builtins.print") as mock_print:
        game.run()

output = "\n".join(
    " ".join(str(arg) for arg in call.args)
    for call in mock_print.call_args_list
)

# Verify both captured pieces were removed.
assert game.board[3][2] == ".", "FAIL: First captured piece remains."
assert game.board[1][4] == ".", "FAIL: Second captured piece remains."

# Verify promotion and turn switching.
assert game.board[0][5] == "RK", "FAIL: Red did not promote."
assert game.player == "B", "FAIL: Turn did not switch."

# Verify the different piece was rejected during the capture chain.
assert (
    "Continue capturing with the same piece." in output
), "FAIL: Different piece was not rejected correctly."

print("PASS: First capture removes the captured piece.")
print("PASS: Different piece is rejected during the capture chain.")
print("PASS: Second capture completes successfully.")
print("PASS: Promotion works after the capture chain.")
print("PASS: Turn switches after the capture chain.")
print("ALL INTERACTIVE MULTI-CAPTURE TESTS PASSED.")