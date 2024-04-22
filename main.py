import tkinter as tk
from tkinter import messagebox, Toplevel, scrolledtext
from constants import WIDTH, HEIGHT, SQUARE_SIZE
from game import Game


def display_rules():
    # Create a top-level window to display rules
    rule_window = Toplevel()
    rule_window.title("Game Rules")
    rule_window.geometry("400x300")  # You can adjust the size as per your content

    # Add a scrolled text widget to make the rules scrollable
    rules_text = scrolledtext.ScrolledText(rule_window, wrap=tk.WORD)
    rules_text.insert(tk.INSERT, """Game Rules:
1. Each player starts with 12 pieces placed on the dark squares of the board closest to them.
2. Players alternate turns, moving one piece per turn (WHITE player is AI with four difficulty levels).
3. A piece can move diagonally forward to an adjacent empty square.
4. A piece can jump over an opponent's adjacent piece if the square beyond is empty. This captures the opponent's piece.
5. If a normal piece reaches the far row from the starting position, it becomes a King. Kings can move forward and backward.
6. If a normal piece captures a King, it is instantly crowned King and the current player's turn ends regardless of any subsequent moves.
7. The game ends when a player cannot make a move, either because all pieces are captured or all remaining pieces are blocked.
8. The player who cannot move loses, and the other player wins.""")
    rules_text.config(state=tk.DISABLED)  # Disable editing of the text
    rules_text.pack(expand=True, fill=tk.BOTH)


def mouse_click(event, game):
    row = event.y // SQUARE_SIZE
    col = event.x // SQUARE_SIZE
    game.select(row, col)


def main():
    root = tk.Tk()
    root.title("Checkers Game")
    root.geometry(f"{WIDTH}x{HEIGHT + 150}")

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack()

    # Difficulty setting
    difficulty_var = tk.StringVar(value='easy')
    difficulties = {'Easy': 'easy', 'Medium': 'medium', 'Hard': 'hard', 'Very Hard': 'very_hard'}
    for text, mode in difficulties.items():
        b = tk.Radiobutton(root, text=text, variable=difficulty_var, value=mode,
                           command=lambda: set_difficulty(difficulty_var.get()))
        b.pack()

    game = Game(canvas, root, difficulty=difficulty_var.get())

    reset_button = tk.Button(root, text="Reset Game", command=game.reset)
    reset_button.pack(side=tk.LEFT, padx=10, pady=10)

    rules_button = tk.Button(root, text="Show Rules", command=display_rules)
    rules_button.pack(side=tk.RIGHT, padx=10, pady=10)

    canvas.bind("<Button-1>", lambda event: mouse_click(event, game))

    def set_difficulty(diff):
        game.difficulty = diff
        game.reset()

    root.mainloop()


if __name__ == "__main__":
    main()
