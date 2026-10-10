from unittest.mock import patch
from game import Checkers

game = Checkers()
game.board = [["."] * 8 for _ in range(8)]

# Red can capture the blue piece at (3, 2).
game.board[4][1] = "R"
game.board[3][2] = "B"

# Another red piece has an ordinary move available.
game.board[5][4] = "R"

# First attempt an ordinary move, then quit.
with patch("builtins.input", side_effect=["5 4 4 5", "q"]):
    with patch("builtins.print") as mock_print:
        game.run()

output = " ".join(
    str(call) for call in mock_print.call_args_list
)

assert "must capture" in output.lower(), (
    "FAIL: The game did not reject the ordinary move."
)

assert game.board[5][4] == "R", (
    "FAIL: The ordinary move was incorrectly applied."
)

assert game.board[4][5] == ".", (
    "FAIL: The ordinary move destination was occupied."
)

print("PASS: Interactive forced-capture enforcement works.")