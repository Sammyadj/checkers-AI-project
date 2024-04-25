from constants import SQUARE_SIZE


class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color, king=False):
        self.row = row
        self.col = col
        self.color = color
        self.king = king
        self.is_highlighted = False
        self.is_valid_move_highlighted = False

        # piece's position on the board
        self.x = 0
        self.y = 0
        self.calc_position()

    # def clone(self):
    #     # Ensure that the board instance is passed to the new cloned piece
    #     new_piece = Piece(self.row, self.col, self.color, self.board, self.crown)
    #     new_piece.king = self.king
    #     new_piece.is_highlighted = self.is_highlighted
    #     new_piece.is_valid_move_highlighted = self.is_valid_move_highlighted
    #     new_piece.calc_position()
    #     return new_piece

    def calc_position(self):
        # Calculate the center of the square
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True
        # if not self.crown:  # Set the crown image from the board if not already set
        #     self.crown = self.board.crown_image

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
        if self.king:
            # canvas.create_image(self.x, self.y, image=self.crown)
            canvas.create_text(self.x, self.y, text="K", fill='black', font=('Arial', 24))

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
