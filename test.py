import unittest
from game import Game
from piece import Piece
from unittest.mock import Mock, patch
from constants import WHITE, RED
from board import Board


class TestCheckersGame(unittest.TestCase):
    def setUp(self):
        mock_canvas = Mock()
        # self.board = Board(mock_canvas)
        with patch('tkinter.PhotoImage', return_value=Mock()):
            self.game = Game(mock_canvas, Mock())
        # self.game.board.setup_board()

    def test_board_cloning(self):
        original_board = self.game.board
        cloned_board = original_board.clone()
        self.assertNotEqual(id(original_board), id(cloned_board), "Cloned board should not be the same instance")
        self.assertEqual(str(original_board), str(cloned_board), "Cloned board should have the same state")

    def test_move_application(self):
        # Move a specific piece and check the result
        start_pos = (5, 2)
        end_pos = (4, 1)
        self.game.board.move_piece(*start_pos, *end_pos)
        self.assertIsNone(self.game.board.get_piece(*start_pos), "Start position should be empty after the move")
        self.assertIsNotNone(self.game.board.get_piece(*end_pos), "End position should have a piece after the move")

    def test_capture_move(self):
        # Setup: Position pieces to set up a capture
        start_pos = (5, 2)
        capture_pos = (4, 3)
        end_pos = (3, 4)

        # Place a piece for the player
        player_piece = Piece(5, 2, RED, self.game.board, False)
        self.game.board.get_square(*start_pos).place_piece(player_piece)
        self.assertIs(self.game.board.get_piece(*start_pos), player_piece, "Player piece should be correctly placed")

        # Place a piece for the opponent
        opponent_piece = Piece(4, 3, WHITE, self.game.board, False)
        self.game.board.get_square(*capture_pos).place_piece(opponent_piece)
        self.assertIs(self.game.board.get_piece(*capture_pos), opponent_piece,
                      "Opponent piece should be correctly placed")

        # Simulate the piece being selected and the valid move being set up
        self.game.turn = RED
        self.game.select(*start_pos)
        self.assertTrue(self.game.selected, "A piece should be selected")
        self.assertTrue(self.game.valid_moves, "Valid moves should be set up")

        # Assert the initial state before the move
        self.assertIsNotNone(self.game.board.get_piece(*start_pos),
                             "Start position should initially have the player piece")
        self.assertIsNotNone(self.game.board.get_piece(*capture_pos),
                             "Capture position should initially have the opponent piece")

        # Execute the move
        moved = self.game._move(start_pos[0], start_pos[1], end_pos[0], end_pos[1])

        # Assert post-move state
        self.assertIsNone(self.game.board.get_piece(*start_pos), "Start position should be empty after the move")
        self.assertIsNone(self.game.board.get_piece(*capture_pos), "Capture position should be empty after the capture")
        self.assertIsNotNone(self.game.board.get_piece(*end_pos),
                             "End position should have the moving piece after the move")
        self.assertTrue(moved, "Move should be executed successfully")

    # def test_minimax_basic(self):
    #     # Set up a board state where the outcome is predictable
    #     # For example, one move away from a win
    #     self.game.board.place_piece(2, 2, 'white')  # Assuming this creates a winning condition on the next move
    #     expected_score = 10  # Example score for a winning move
    #     score = self.game.minimax(self.game.board, 1, -float('inf'), float('inf'), True)
    #     self.assertEqual(score, expected_score, "Minimax should return the correct score for a winning move")

    # def test_alpha_beta_pruning(self):
    #     # Test that alpha-beta pruning reduces the number of recursive calls
    #     initial_call_count = self.game.call_count
    #     self.game.minimax(self.game.board, 3, -float('inf'), float('inf'), True)
    #     pruned_call_count = self.game.call_count
    #     self.assertLess(pruned_call_count, initial_call_count, "Alpha-beta pruning should reduce the number of minimax calls")


# Run the tests
if __name__ == '__main__':
    unittest.main()
