# simulation.py
from game import Game


def play_game(game1, game2):
    current_game = game1
    opponent_game = game2
    move_limit = 200  # Prevent infinite loops
    move_count = 0

    while move_count < move_limit:
        # Get best move for current AI
        best_move = current_game.ai_move()
        if best_move is None:
            # No valid moves, opponent wins
            return opponent_game.difficulty

        # Execute the move
        current_game.execute_move(best_move)

        # Check for winner
        if current_game.check_winner():
            return current_game.difficulty

        # Swap players
        current_game, opponent_game = opponent_game, current_game
        move_count += 1

    # If no winner after move_limit, declare draw or handle according to specific rules
    return 'draw'


def run_simulations():
    game1 = Game(difficulty='easy', simulation_mode=True)
    game2 = Game(difficulty='medium', simulation_mode=True)
    winner = play_game(game1, game2)
    print(f"The winner is {winner}")

if __name__ == "__main__":
    run_simulations()

