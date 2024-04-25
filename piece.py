from constants import SQUARE_SIZE


class Piece:
    """A class to represent a checkers piece on the board.
    Attributes:
        row (int): The row index of the piece on the board.
        col (int): The column index of the piece on the board.
        color (str): The color of the piece ('white' or 'red').
        board (Board): The board instance on which the piece is placed.
        king (bool): A boolean flag to indicate if the piece is a king.
        crown (PhotoImage): The crown image to display on a king piece.
        is_highlighted (bool): A boolean flag to indicate if the piece is highlighted.
        is_valid_move_highlighted (bool): A boolean flag to indicate if the piece is highlighted as a valid move.
        x (int): The x-coordinate of the piece on the board.
        y (int): The y-coordinate of the piece on the board."""
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color, board, crown_image=None):
        self.row = row
        self.col = col
        self.color = color
        self.board = board
        self.king = False
        self.crown = crown_image if crown_image else board.crown_image
        self.is_highlighted = False
        self.is_valid_move_highlighted = False

        # piece's position on the board
        self.x = 0
        self.y = 0
        self.calc_position()


    def clone(self):
        # Ensure that the board instance is passed to the new cloned piece
        new_piece = Piece(self.row, self.col, self.color, self.board, self.crown)
        new_piece.king = self.king
        new_piece.is_highlighted = self.is_highlighted
        new_piece.is_valid_move_highlighted = self.is_valid_move_highlighted
        new_piece.calc_position()
        return new_piece

    def calc_position(self):
        # Calculate the center of the square
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    # def make_king(self):
    #     self.king = True
    #     print(f"Made {self.color} piece at ({self.row}, {self.col}) a king.")

    def make_king(self):
        self.king = True
        if not self.crown:  # Set the crown image from the board if not already set
            self.crown = self.board.crown_image

    def draw(self, canvas):
        # Calculate the radius for the piece
        radius = SQUARE_SIZE // 2 - self.PADDING

        # Draw the piece
        canvas.create_oval(
            self.x - radius, self.y - radius,
            self.x + radius, self.y + radius,
            fill=self.color,
            outline='yellow' if self.is_highlighted else '',
            width=4 if self.is_highlighted else 0
        )

        # If the piece is valid for a move, draw an additional highlight
        if self.is_valid_move_highlighted:
            canvas.create_oval(
                self.x - radius - 5, self.y - radius - 5,
                self.x + radius + 5, self.y + radius + 5,
                outline='green', width=2
            )

        # If the piece is a king, draw the crown image on top of it
        if self.king and self.crown:
            print("Drawing crown image.")
            canvas.create_image(self.x, self.y, image=self.crown)

    def toggle_highlight(self):
        self.is_highlighted = not self.is_highlighted  # Toggle the highlight state

    def highlight_valid_move(self):
        self.is_valid_move_highlighted = True

    def unhighlight_valid_move(self):
        self.is_valid_move_highlighted = False

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_position()  # Update the piece's position on the board

    def __repr__(self):
        return f"{'White' if self.color == 'white' else 'Red'} {'King' if self.king else 'Man'}"

    def __str__(self):
        return str(self.color)
