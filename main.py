import tkinter as tk
from tkinter import messagebox, Toplevel, scrolledtext
from constants import WIDTH, HEIGHT, SQUARE_SIZE
from game import Game


def display_instructions():
    messagebox.showinfo("Instructions", """Game interactivity:
- You can click on a piece to select it.
- Click on a highlighted square to move the selected piece.
- Click on the selected piece again to deselect it.
- Click on the 'Reset Game' button to start a new game.
- Click on the 'Show Rules' button to display the game rules.
- Use the radio buttons to change the AI difficulty.""")


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


def main():
    root = tk.Tk()
    root.title("Checkers Game")
    root.geometry(f"{WIDTH}x{HEIGHT + 85}")

    top_frame = tk.Frame(root)
    top_frame.pack(side=tk.TOP, fill=tk.X)

    bottom_frame = tk.Frame(root)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

    difficulty_frame = tk.Frame(bottom_frame)
    difficulty_frame.pack(side=tk.TOP, fill=tk.X)

    status_bar = tk.Label(bottom_frame, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.TOP, fill=tk.X)

    canvas = tk.Canvas(root, width=800, height=800)
    canvas.pack(expand=True, fill=tk.BOTH)

    game = Game(canvas, root)

    reset_button = tk.Button(top_frame, text="Reset Game", command=lambda: game.set_difficulty(game.difficulty))
    reset_button.pack(side=tk.LEFT, padx=5, pady=5)

    rules_button = tk.Button(top_frame, text="Show Rules", command=display_rules)
    rules_button.pack(side=tk.LEFT, padx=5, pady=5)

    instructions_button = tk.Button(top_frame, text="Instructions", command=display_instructions)
    instructions_button.pack(side=tk.LEFT, padx=5, pady=5)

    difficulty_var = tk.StringVar(value='easy')
    difficulties = {'Easy': 'easy', 'Medium': 'medium', 'Hard': 'hard', 'Very Hard': 'very_hard'}
    for text, mode in difficulties.items():
        b = tk.Radiobutton(difficulty_frame, text=text, variable=difficulty_var, value=mode,
                           command=lambda m=mode: game.set_difficulty(m))
        b.pack(side=tk.LEFT, padx=5, pady=5)

    def show_message(message):
        status_bar.config(text=message)

    def mouse_click(event):
        row = event.y // 100  # Placeholder for square size
        col = event.x // 100
        valid, msg = game.select(row, col)
        show_message(msg)

    canvas.bind("<Button-1>", mouse_click)

    root.mainloop()

if __name__ == "__main__":
    main()


# def main():
#     root = tk.Tk()
#     root.title("Checkers Game")
#     root.geometry(f"{WIDTH}x{HEIGHT + 150}")
#
#     canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
#     canvas.pack()
#
#     status_bar = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
#     status_bar.pack(side=tk.BOTTOM, fill=tk.X)
#
#     def show_message(message):
#         status_bar.config(text=message)
#
#     def mouse_click(event, game):
#         row = event.y // SQUARE_SIZE
#         col = event.x // SQUARE_SIZE
#         valid, msg = game.select(row, col)
#         show_message(msg)
#
#     game = Game(canvas, root, difficulty='easy')  # Assuming default difficulty is 'easy'
#
#     reset_button = tk.Button(root, text="Reset Game", command=lambda: [game.reset(), show_message("Game reset!")])
#     reset_button.pack(side=tk.LEFT, padx=10, pady=10)
#
#     rules_button = tk.Button(root, text="Show Rules", command=display_rules)
#     rules_button.pack(side=tk.RIGHT, padx=10, pady=10)
#
#     instructions_button = tk.Button(root, text="Instructions", command=dislay_instructions)
#     instructions_button.pack(side=tk.RIGHT, padx=10, pady=10)
#
#     difficulty_var = tk.StringVar(value='easy')
#     difficulties = {'Easy': 'easy', 'Medium': 'medium', 'Hard': 'hard', 'Very Hard': 'very_hard'}
#     for text, mode in difficulties.items():
#         b = tk.Radiobutton(root, text=text, variable=difficulty_var, value=mode,
#                            command=lambda m=mode: [game.set_difficulty(m), show_message(f"Difficulty set to {m}")])
#         b.pack()
#
#     canvas.bind("<Button-1>", lambda event: mouse_click(event, game))
#
#     root.mainloop()
#
#
# if __name__ == "__main__":
#     main()

