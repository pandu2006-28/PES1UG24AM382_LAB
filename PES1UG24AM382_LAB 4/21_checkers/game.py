
from board import initial_board, move_piece, SIZE
from rules import (
    simple_move,
    capture_move,
    promote,
    has_pieces,
    has_legal_move,
    has_capture,
)


class Checkers:
    def __init__(self):
        self.board = initial_board()
        self.player = "R"
        self.continue_capture = False
        self.last_capture_position = None

    def print_board(self):
        print("\n   " + " ".join(str(c) for c in range(SIZE)))
        for r, row in enumerate(self.board):
            print(f"{r}  " + " ".join(row))

    def run(self):
        print("Checkers — move: sr sc er ec (or q to quit)")

        while True:
            self.print_board()
            raw = input(f"{self.player}> ").strip().lower().split()

            if raw == ["q"]:
                print("Game ended.")
                return

            if len(raw) != 4:
                print("Enter four coordinates.")
                continue

            try:
                sr, sc, er, ec = map(int, raw)
            except ValueError:
                print("Coordinates must be numbers.")
                continue

            if not all(0 <= x < SIZE for x in (sr, sc, er, ec)):
                print("Outside board.")
                continue

            start, end = (sr, sc), (er, ec)
            piece = self.board[sr][sc]

            if piece not in (self.player, self.player + "K"):
                print("That is not your piece.")
                continue

            if self.continue_capture and start != self.last_capture_position:
                print("Continue capturing with the same piece.")
                continue

            is_capture = capture_move(
                self.board, self.player, start, end
            )

            # Captures are compulsory.
            if has_capture(self.board, self.player) and not is_capture:
                print("A capture is available. You must capture.")
                continue

            if not is_capture and not simple_move(
                self.board, self.player, start, end
            ):
                print("Invalid move.")
                continue

            # Record whether this move causes promotion.
            moving_piece = self.board[sr][sc]
            move_piece(self.board, start, end)
            promote(self.board)
            promoted = (
                moving_piece in ("R", "B")
                and self.board[er][ec] in ("RK", "BK")
            )

            # Check for another capture before ending the turn.
            if is_capture and has_capture(
                self.board, self.player, end
            ):
                self.continue_capture = True
                self.last_capture_position = end

                if promoted:
                    print(
                        f"{self.player} captures and promotes to "
                        f"{self.board[er][ec]}."
                    )
                else:
                    print(f"{self.player} captures a piece.")

                print("Another capture is available; continue your turn.")
                continue

            # One concise result for the accepted move.
            if is_capture and promoted:
                print(
                    f"{self.player} captures and promotes to "
                    f"{self.board[er][ec]}."
                )
            elif is_capture:
                print(f"{self.player} captures a piece.")
            elif promoted:
                print(
                    f"{self.player} moves to ({er}, {ec}) "
                    f"and promotes to {self.board[er][ec]}."
                )
            else:
                print(f"{self.player} moves to ({er}, {ec}).")

            self.continue_capture = False
            self.last_capture_position = None

            # Switch turns only after the move sequence finishes.
            self.player = "B" if self.player == "R" else "R"

            if not has_pieces(self.board, self.player):
                winner = "R" if self.player == "B" else "B"
                self.print_board()
                print(f"{winner} wins! The opponent has no pieces left.")
                return

            if not has_legal_move(self.board, self.player):
                winner = "R" if self.player == "B" else "B"
                self.print_board()
                print(f"{winner} wins! The opponent has no legal moves.")
                return
