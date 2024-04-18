import tkinter as tk
from constants import ROWS, COLS, BLACK, WHITE, RED, GREY, SQUARE_SIZE, CROWN
from piece import Piece


class Square:
    def __init__(self, piece=None):
        self.piece = piece
        self.row = None
        self.col = None

    def clone(self):
        new_square = Square()
        if self.piece:
            new_square.piece = self.piece.clone()
        new_square.row = self.row
        new_square.col = self.col
        return new_square

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def place_piece(self, piece):
        self.piece = piece

    def remove_piece(self):
        self.piece = None

    def is_occupied(self):
        return self.piece is not None

    def __repr__(self):
        if self.piece:
            return f"{self.piece}"
        return "Empty"


class Board:
    def __init__(self, game=None):
        self.game = game
        self.crown_image = None
        self.board = [[Square() for _ in range(COLS)] for _ in range(ROWS)]  # 8x8 board
        self.red_left = self.white_left = 12  # Number of pieces each player has
        self.red_kings = self.white_kings = 0
        # self.load_images()
        self.setup_board()

    def clone(self):
        new_board = Board()
        new_board.game = self.game  # Maintain the same game reference
        new_board.crown_image = self.crown_image  # Maintain the same image reference
        new_board.red_left = self.red_left
        new_board.white_left = self.white_left
        new_board.red_kings = self.red_kings
        new_board.white_kings = self.white_kings

        for i in range(ROWS):
            for j in range(COLS):
                new_board.board[i][j] = self.board[i][j].clone()  # Use the new clone method for squares

        return new_board

    def load_images(self):
        # if not self.crown_image:
        #     self.crown_image = tk.PhotoImage(file=CROWN).subsample(64, 64)
        try:
            self.crown_image = tk.PhotoImage(file=CROWN).subsample(64, 64)
        except Exception as e:
            print(f"Failed to load crown image: {e}")

    @staticmethod
    def draw_squares(canvas):
        canvas.config(bg=GREY)
        for row in range(ROWS):
            for col in range((row + 1) % 2, ROWS, 2):
                x0 = col * SQUARE_SIZE
                y0 = row * SQUARE_SIZE
                x1 = x0 + SQUARE_SIZE
                y1 = y0 + SQUARE_SIZE
                canvas.create_rectangle(x0, y0, x1, y1, fill=BLACK, outline="")

    def setup_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                if row % 2 == ((col + 1) % 2):
                    if row < 3:
                        piece = Piece(row, col, WHITE, self, self.crown_image)
                        self.board[row][col].place_piece(piece)
                    elif row > 4:
                        piece = Piece(row, col, RED, self, self.crown_image)
                        self.board[row][col].place_piece(piece)

    def draw(self, canvas):
        try:
            self.draw_squares(canvas)
            for row in self.board:
                for square in row:
                    if square and square.is_occupied():
                        square.piece.draw(canvas)
        except Exception as e:
            print(f"Error drawing board: {e}")
            raise e

    def move_piece(self, start_row, start_col, end_row, end_col):
        piece = self.get_piece(start_row, start_col)
        if piece and not self.is_square_occupied(end_row, end_col):
            # Move the piece
            self.board[end_row][end_col].place_piece(piece)
            self.board[start_row][start_col].remove_piece()

            # Update the piece's position
            piece.move(end_row, end_col)

            # Promote to king if it reaches the last row and is not already a king
            if end_row in [0, ROWS - 1] and not piece.king:
                print("Assigning crown image to a white piece.")
                piece.make_king()
                if piece.color == RED:
                    self.red_kings += 1
                    print(f"Red kings increased in white king's row: {self.red_kings}")
                else:
                    self.white_kings += 1
                    print(f"White kings increased in white king's row: {self.white_kings}")

    # Remove the captured piece(s) from the board
    def remove(self, captures, capturing_piece):
        regicide_occurred = False
        for row, col in captures:
            piece = self.get_piece(row, col)
            if piece:
                self.update_pieces_left(piece)  # Update the count of pieces left
                self.get_square(row, col).remove_piece()  # Remove the captured piece from the board
                if piece.king and not capturing_piece.king:
                    capturing_piece.make_king()  # Promote the capturing piece if it captures a king
                    regicide_occurred = True
                    if capturing_piece.color == RED:
                        self.red_kings += 1
                        print(f"Red kings increased by regicide: {self.red_kings}")
                    else:
                        self.white_kings += 1
                        print(f"White kings increased by regicide: {self.white_kings}")
        return regicide_occurred

    def update_pieces_left(self, piece):
        if piece.color == RED:
            self.red_left -= 1
            print(f"Red pieces left: {self.red_left}")
            if piece.king:
                self.red_kings -= 1
                print(f"Red kings left: {self.red_kings}")
        else:
            self.white_left -= 1
            print(f"White pieces left: {self.white_left}")
            if piece.king:
                self.white_kings -= 1
                print(f"White kings left: {self.white_kings}")

    def winner(self):
        # Check if either player has no pieces left
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED

        # Check for no available moves for either player
        # We assume that this method is called after a player's turn is complete
        red_moves_available = self.check_moves_available(RED)
        white_moves_available = self.check_moves_available(WHITE)

        if not red_moves_available:
            return WHITE  # White wins if Red has no moves
        if not white_moves_available:
            return RED  # Red wins if White has no moves

        return None  # No winner yet

    def check_moves_available(self, color):
        # Iterate over all squares to find pieces of the given color
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                piece = self.get_piece(row, col)
                if piece and piece.color == color:
                    # Check if there are any valid moves for this piece
                    if self.get_valid_moves(piece, row, col):
                        return True  # There is at least one move available
        return False  # No moves available for this color

    # HELPER FUNCTIONS:
    # Check if the square is occupied
    def is_square_occupied(self, row, col):
        if 0 <= row < len(self.board) and 0 <= col < len(self.board[row]):
            square = self.board[row][col]
            if square is not None and square.piece:
                return True
        return False

    # Get the square at the given row and column
    def get_square(self, row, col):
        """Return the Square object at the specified location on the board"""
        try:
            return self.board[row][col]
        except IndexError:
            return None

    @staticmethod
    def _on_board(row, col):
        return 0 <= row < ROWS and 0 <= col < COLS

    def get_piece(self, row, col):
        """Return the Piece object at the specified location on the board"""
        if self._on_board(row, col):
            return self.board[row][col].piece
        return None

    # Check if the square is occupied by an opponent piece
    def is_opponent(self, piece, row, col):
        opponent = self.get_piece(row, col)
        return opponent and opponent.color != piece.color

    # Check if a piece can capture an opponent piece
    def can_capture(self, piece, next_row, next_col, jump_row, jump_col, visited):
        # Ensure both the intermediate and jump positions are within board boundaries
        if not (self._on_board(next_row, next_col) and self._on_board(jump_row, jump_col)):
            return False

        # Check if the intermediate square has an opponent's piece
        if not self.is_opponent(piece, next_row, next_col):
            return False

        # Check if the jump position is unoccupied and not previously visited
        if self.is_square_occupied(jump_row, jump_col) or (jump_row, jump_col) in visited:
            return False

        # All conditions are met, capture is possible
        return True

    @staticmethod
    def get_movement_directions(piece):
        if piece.king:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Kings move in all four diagonal directions
        else:
            return [(1, -1), (1, 1)] if piece.color == WHITE else [(-1, -1),
                                                                   (-1, 1)]  # Non-kings move forward diagonally

    # MOVES AND CAPTURES LOGIC:
    # Get the valid moves for the selected piece
    def get_valid_moves(self, piece, row, col):
        valid_moves = {}
        captures = self.compute_capture_paths(piece, row, col)

        # Check if there are any captures, if not, consider normal moves
        if not any(captures.values()):  # If there are no capture paths
            directions = self.get_movement_directions(piece)
            for dr, dc in directions:
                next_row = row + dr
                next_col = col + dc
                if self._on_board(next_row, next_col) and not self.is_square_occupied(next_row, next_col):
                    # Add the move as a key with an empty dictionary for its value
                    valid_moves[(next_row, next_col)] = {
                        'captures': [],
                        'landing_positions': []
                    }
        else:
            valid_moves.update(captures)
        return valid_moves

    def compute_capture_paths(self, piece, start_row, start_col, path=None, visited=None, captures=None):
        if path is None:
            path = []
        if visited is None:
            visited = set()
        if captures is None:
            captures = []

        moves = {}
        directions = self.get_movement_directions(piece)
        for dr, dc in directions:
            next_row, next_col = start_row + dr, start_col + dc
            jump_row, jump_col = start_row + 2 * dr, start_col + 2 * dc
            if self._on_board(next_row, next_col) and self._on_board(jump_row, jump_col):
                if (jump_row, jump_col) not in visited and self.can_capture(piece, next_row, next_col, jump_row,
                                                                            jump_col, visited):
                    visited.add((jump_row, jump_col))  # Prevent revisiting
                    captures.append((next_row, next_col))
                    new_path = path + [(jump_row, jump_col)]
                    subsequent_captures = self.compute_capture_paths(
                        piece, jump_row, jump_col, new_path, visited.copy(), captures.copy())

                    if subsequent_captures:
                        moves.update(subsequent_captures)
                    else:
                        moves[(jump_row, jump_col)] = {
                            'captures': captures.copy(),
                            'landing_positions': path.copy()
                        }
                    # Backtracking: Remove the last capture
                    captures.pop()
                    visited.remove((jump_row, jump_col))
        return moves

    def __repr__(self):
        return f"{self.board}"
