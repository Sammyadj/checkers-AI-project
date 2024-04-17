import tkinter as tk
from constants import WIDTH, HEIGHT, SQUARE_SIZE
from game import Game


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

    game = Game(canvas, difficulty=difficulty_var.get())
    game.board.load_images()

    reset_button = tk.Button(root, text="Reset Game", command=game.reset)
    reset_button.pack()

    canvas.bind("<Button-1>", lambda event: mouse_click(event, game))

    def set_difficulty(diff):
        game.difficulty = diff
        game.reset()

    root.mainloop()


if __name__ == "__main__":
    main()
