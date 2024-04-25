from constants import RED, WHITE, ROWS, COLS, SQUARE_SIZE
from board import Board
from tkinter import messagebox
import traceback
import time


class Game:
    def __init__(self, canvas, root, difficulty='easy'):
        self.canvas = canvas
        self.root = root
        self.difficulty = difficulty
        self.sorted_moves = None
        self._init()

    def _init(self):

        self.selected = None
        self.board = Board(self)
        self.board.load_images()
        self.turn = RED
        self.valid_moves = {}  # Store the valid moves for the selected piece
        player_valid_moves = self.find_player_valid_moves()
        self.highlight_pieces_with_moves(player_valid_moves)
        self.update()

    def update(self):
        # print("Update called from:", traceback.extract_stack()[-2].name)
        # # traceback.print_stack(limit=2)
        self.board.draw(self.canvas)
        self.draw_valid_moves(self.valid_moves)  # Draw the valid moves
        if self.turn == WHITE:
            print("AI is thinking...")

    def reset(self):
        self._init()

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.reset()  # Reset the game state when the difficulty changes

    def select(self, row, col):
        # Retrieve the piece at the clicked square (if any)
        current_piece = self.board.get_piece(row, col)

        # Check if there is no piece at the selected square and no piece currently selected
        if not current_piece and not self.selected:
            return False, "No piece at the selected square."

        # Check if the same piece is clicked again (deselect if so)
        if self.selected == (row, col):
            current_piece.toggle_highlight()
            self.valid_moves = {}  # Clear valid moves since we are deselecting
            self.selected = None
            self.update()  # Update the UI to reflect the deselection
            return False, "Piece deselected."

        # Retrieve all valid moves for the current player
        valid_moves = self.find_player_valid_moves()

        # If a piece is already selected and a new square is clicked
        if self.selected and (row, col) != self.selected:
            selected_row, selected_col = self.selected

            # If the new square is within the valid moves, perform the move
            if (row, col) in self.valid_moves:
                self._move(selected_row, selected_col, row, col)
                self.selected = None  # Deselect the piece after moving
                self.update()  # Update the UI to reflect the new board state
                return True, f"Move performed successfully to {row}, {col}"

            # If another piece is clicked and it's a valid move, switch selection
            elif current_piece and current_piece.color == self.turn and (row, col) in valid_moves:
                self.board.get_piece(selected_row,
                                     selected_col).toggle_highlight()  # Remove highlight from previously selected piece
                current_piece.toggle_highlight()  # Highlight the newly selected piece
                self.selected = (row, col)
                self.valid_moves = valid_moves[(row, col)]
                self.update()  # Update the UI to show the new selection
                return True, f"Selection changed to {row}, {col}"

            # If the click is neither a valid move nor a valid selection, return an error
            else:
                return False, "Invalid move: Move not allowed."

        # If a piece of the current player's color is clicked, select it
        elif current_piece and current_piece.color == self.turn and (row, col) in valid_moves:
            current_piece.toggle_highlight()  # Highlight the clicked piece
            self.selected = (row, col)
            self.valid_moves = valid_moves[(row, col)]
            self.update()  # Update the UI to show the selection
            return True, f"Piece selected at {row}, {col}"

        # If none of the above conditions are met, return a generic error message
        self.update()  # Update the UI in case there are other changes to reflect
        return False, "It's not your turn or piece cannot be moved."

    def _move(self, start_row, start_col, end_row, end_col):
        """Move the selected piece to the target square if the move is valid.
        If a capture move is available, the piece must make the capture.
        If a piece is captured, it is removed from the board."""
        if self.selected and (end_row, end_col) in self.valid_moves: # Ensure a valid move is selected
            moving_piece = self.board.get_piece(start_row, start_col)
            moving_piece.toggle_highlight()  # Toggle highlight off before moving
            self.board.move_piece(start_row, start_col, end_row, end_col)

            move_info = self.valid_moves[(end_row, end_col)]
            captures = move_info['captures']
            if captures: # If a capture move is made, remove the captured pieces
                regicide_occurred = self.board.remove(captures, moving_piece)
                if regicide_occurred:  # If a normal piece captures a King, it is instantly crowned King
                    self.end_turn()
                    return True
            self.end_turn()

            return True
        return False

    def draw_valid_moves(self, valid_moves):  # Draw valid moves on the board
        for final_move, move_info in valid_moves.items():
            # captures = move_info.get('captures', [])
            landing_positions = move_info.get('landing_positions', [])

            # Draw the final landing position with a distinctive style
            final_row, final_col = final_move
            final_x = final_col * SQUARE_SIZE + SQUARE_SIZE // 2
            final_y = final_row * SQUARE_SIZE + SQUARE_SIZE // 2
            self.canvas.create_oval(
                final_x - 10, final_y - 10, final_x + 10, final_y + 10,
                outline='green', fill='green', width=1.5
            )

            # Draw intermediate landing positions
            for land_pos in landing_positions:
                land_row, land_col = land_pos
                land_x = land_col * SQUARE_SIZE + SQUARE_SIZE // 2
                land_y = land_row * SQUARE_SIZE + SQUARE_SIZE // 2
                self.canvas.create_oval(
                    land_x - 8, land_y - 8, land_x + 8, land_y + 8,
                    outline='blue', fill='', width=2
                )

    def find_player_valid_moves(self):
        """Find all valid moves for the current player. If any captures are available, only return capture moves.
        Otherwise, return all valid moves."""
        player_valid_moves = {}
        player_capture_moves = {}
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == self.turn:
                    valid_moves = self.board.get_valid_moves(piece, row, col)
                    if any(move_info['captures'] for move_info in valid_moves.values()):
                        player_capture_moves[(row, col)] = valid_moves
                    else:
                        player_valid_moves[(row, col)] = valid_moves
        return player_capture_moves if player_capture_moves else player_valid_moves

    def highlight_pieces_with_moves(self, valid_moves): # Highlight pieces with valid moves
        for position, moves in valid_moves.items():
            piece = self.board.get_piece(*position)
            if moves:
                piece.highlight_valid_move()

    def clear_valid_move_highlights(self):  # Clear highlights from all pieces
        if self.board is not None:
            for row in range(ROWS):
                for col in range(COLS):
                    piece = self.board.get_piece(row, col)
                    if piece and piece.is_valid_move_highlighted:
                        piece.unhighlight_valid_move()

    def check_winner(self, board=None):
        if board is None:
            board = self.board
        if not board:
            return False
        winner = board.winner()
        if winner:
            self.winner = winner
            return True
        return False

    # Update the game state upon turn change
    def change_turn(self):
        self.turn = RED if self.turn == WHITE else WHITE
        self.valid_moves = {}
        self.clear_valid_move_highlights()  # Clear highlights from all pieces
        # Check if the next player is AI and trigger AI move
        if self.turn == WHITE:
            self.root.after(50, self.ai_turn)
        else:
            player_valid_moves = self.find_player_valid_moves()
            self.highlight_pieces_with_moves(player_valid_moves)

    def end_turn(self):
        self.selected = None
        self.change_turn()
        self.update()
        self.root.after(50, self.post_update_check_winner)  # Short delay to update UI before checking winner

    def post_update_check_winner(self):
        if self.check_winner():
            self.handle_game_end()

    def handle_game_end(self):
        # Disable further interactions or reset the game here if needed
        self.update()
        print(f"{self.winner} has won the game!")
        messagebox.showinfo("Game Over", f"{self.winner} has won the game! Press 'Reset Game' to play again.")
        self.root.after(100, self.reset)

    def ai_turn(self):
        """AI makes a move based on the selected difficulty level.
        The AI uses the minimax algorithm with alpha-beta pruning to determine the best move."""
        if self.check_winner():
            return
        best_score = float('-inf')
        # best_move = None
        best_board = None
        for move, cloned_board in self.get_successors(self.board):
            score = self.minimax(cloned_board, 6, -float('inf'), float('inf'), True)
            if score > best_score:
                best_score = score
                # best_move = move
                best_board = cloned_board

        # AI's move results in a new board state that should be committed
        if best_board is not None:
            self.board = best_board
            print("AI moved")
        else:
            print("No valid moves available for AI")
        self.end_turn()

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.check_winner(board):
            return self.evaluate(board)

        if maximizing_player:
            max_eval = float('-inf')
            for _, successor in self.get_successors(board):
                _eval = self.minimax(successor, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, _eval)
                alpha = max(alpha, _eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for _, successor in self.get_successors(board):
                _eval = self.minimax(successor, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, _eval)
                beta = min(beta, _eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_successors(self, board):
        successors = []
        valid_moves = self.find_player_valid_moves()
        for pos, moves_dict in valid_moves.items():
            for move, details in moves_dict.items():
                cloned_board = board.clone()
                moving_piece = cloned_board.get_piece(pos[0], pos[1])
                cloned_board.move_piece(pos[0], pos[1], move[0], move[1])
                captures = details.get('captures', [])
                if captures:
                    cloned_board.remove(captures, moving_piece)
                successors.append((move, cloned_board))
        return successors

    # HEURISTIC EVALUATION FUNCTION WITH DIFFICULTY LEVELS
    def evaluate(self, board):
        if self.difficulty == 'easy':
            return self.evaluate_simple(board)
        elif self.difficulty == 'medium':
            return self.evaluate_strategic(board)
        elif self.difficulty == 'hard':
            return self.evaluate_defensive(board)
        elif self.difficulty == 'very_hard':
            return self.evaluate_comprehensive(board)

    def evaluate_simple(self, board):
        score = (board.white_left - board.red_left) + (board.white_kings * 1.5 - board.red_kings * 1.5)
        return score if self.turn == WHITE else -score

    def evaluate_strategic(self, board):
        score = 0
        for row in range(len(board.board)):
            for col in range(len(board.board[row])):
                piece = board.get_piece(row, col)
                if piece:
                    # Calculate positional and mobility values as before
                    position_value = 1 + (7 - abs(3.5 - col)) * 0.1
                    moves = len(board.get_valid_moves(piece, row, col))
                    mobility_value = moves * 0.1

                    # Check for vulnerability
                    if self.piece_vulnerable(board, piece, row, col):
                        vulnerability_penalty = -3  # Assign a penalty for risky positions

                        # Apply calculated values
                        piece_value = (position_value + mobility_value + (
                            vulnerability_penalty if piece.color == WHITE else -vulnerability_penalty))
                        score += piece_value if piece.color == WHITE else -piece_value

        return score if self.turn == WHITE else -score

    def piece_vulnerable(self, board, piece, row, col):
        # Simulate moving the piece to the position and check if any opponent moves can capture it
        original_row, original_col = piece.row, piece.col
        # Temporarily move the piece
        board.board[original_row][original_col].remove_piece()
        board.board[row][col].place_piece(piece)
        opponent_color = RED if piece.color == WHITE else WHITE

        # Check all opponent moves for captures
        for orow in range(len(board.board)):
            for ocol in range(len(board.board[orow])):
                opponent_piece = board.get_piece(orow, ocol)
                if opponent_piece and opponent_piece.color == opponent_color:
                    if any(move['captures'] for move in board.get_valid_moves(opponent_piece, orow, ocol).values()):
                        # Restore the piece to its original position
                        board.board[row][col].remove_piece()
                        board.board[original_row][original_col].place_piece(piece)
                        return True

        # Restore the piece to its original position
        board.board[row][col].remove_piece()
        board.board[original_row][original_col].place_piece(piece)
        return False

    def evaluate_defensive(self, board):
        score = 0
        for row in range(len(board.board)):
            for col in range(len(board.board[row])):
                piece = board.get_piece(row, col)
                if piece:
                    # Basic piece value
                    base_value = 1 if not piece.king else 1.5

                    # Edge protection value
                    edge_value = 0.1 if col == 0 or col == len(board.board[0]) - 1 else 0

                    # Back row protection
                    back_row_value = 0.2 if (piece.color == WHITE and row == 0) or (
                            piece.color == RED and row == len(board.board) - 1) else 0

                    # Center control (more central pieces are given a slight bonus)
                    center_value = 1 - abs(3.5 - col) * 0.05  # Decreases as you move away from the center

                    # Set trap value
                    trap_value = 0.5 if piece.color == WHITE and row == 0 and (
                            col == 0 or col == len(board.board[0]) - 1) else 0

                    # Incentivize moving closer to becoming a king
                    kinging_advantage = 0.3 if (piece.color == WHITE and row < 3) or (
                            piece.color == RED and row > 4) else 0

                    # Penalize allowing the opponent to king
                    opponent_kinging_risk = -0.5 if (piece.color == WHITE and row > 5) or (
                            piece.color == RED and row < 2) else 0

                    # Calculate total piece value
                    piece_value = base_value + edge_value + back_row_value + center_value + trap_value + kinging_advantage + opponent_kinging_risk
                    if piece.color == WHITE:
                        score += piece_value
                    else:
                        score -= piece_value

        return score if self.turn == WHITE else -score

    def evaluate_comprehensive(self, board):
        score = 0
        for row in range(len(board.board)):
            for col in range(len(board.board[row])):
                piece = board.get_piece(row, col)
                if piece:
                    # Define base values
                    base_value = 5 if not piece.king else 7.75

                    # Back row defense value
                    back_row_value = 4 if (piece.color == WHITE and row == 7) or (
                            piece.color == RED and row == 0) else 0

                    # Middle control values
                    middle_box_value = 2.5 if (2 <= row <= 5) and (2 <= col <= 5) else 0
                    middle_row_value = 0.5 if (2 <= row <= 5) and not (2 <= col <= 5) else 0

                    # Vulnerability check
                    vulnerable_value = -3 if self.is_piece_vulnerable(piece, row, col) else 0

                    # Protection check
                    protected_value = 3 if self.is_piece_protected(piece, row, col) else 0

                    # Calculate total piece value considering all factors
                    piece_value = (base_value + back_row_value + middle_box_value +
                                   middle_row_value + vulnerable_value + protected_value)

                    if piece.color == WHITE:
                        score += piece_value
                    else:
                        score -= piece_value

        return score if self.turn == WHITE else -score

    def is_piece_vulnerable(self, piece, row, col):
        directions = self.board.get_movement_directions(piece)
        for dr, dc in directions:
            enemy_row, enemy_col = row + dr, col + dc
            landing_row, landing_col = row + 2 * dr, col + 2 * dc

            if self.board.can_capture(piece, enemy_row, enemy_col, landing_row, landing_col, set()):
                return True  # The piece can be jumped and captured
        return False

    def is_piece_protected(self, piece, row, col):
        # Check for friendly pieces directly adjacent in a way that blocks enemy jumps
        directions = [(-dr, -dc) for dr, dc in
                      self.board.get_movement_directions(piece)]  # Reverse directions for potential protectors
        for dr, dc in directions:
            opponent_row, opponent_col = row + dr, col + dc
            if self.board._on_board(opponent_row, opponent_col):
                friend_piece = self.board.get_piece(opponent_row, opponent_col)
                if friend_piece and friend_piece.color == piece.color:
                    return True  # Protected by another friendly piece

        # Also consider pieces that could jump into position to protect if attacked
        for dr, dc in self.board.get_movement_directions(piece):
            if self.can_protect(piece, row, col, row + dr, col + dc):
                return True

        return False

    def can_protect(self, piece, current_row, current_col, check_row, check_col):
        if not self.board._on_board(check_row, check_col):
            return False  # Target position must be on the board

        if self.board.is_square_occupied(check_row, check_col):
            return False  # Target position must be unoccupied

        # If piece is a king, it can move in any direction; otherwise, ensure it moves forward
        if not piece.king:
            if piece.color == 'WHITE' and check_row <= current_row:
                return False  # White regular pieces must move upward
            if piece.color == 'RED' and check_row >= current_row:
                return False  # Red regular pieces must move downward

        return True  # The move is possible and could potentially protect another piece
