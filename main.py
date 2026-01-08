from dataclasses import dataclass
import random


@dataclass
class GameState:
    round_number: int = 1
    user_score: int = 0
    bot_score: int = 0
    user_bomb_used: bool = False
    bot_bomb_used: bool = False
    game_over: bool = False


def validate_move(move: str, bomb_used: bool):
    move = move.lower().strip()
    valid_moves = {"rock", "paper", "scissors", "bomb"}

    if move not in valid_moves:
        return False, "Invalid move. Use rock, paper, scissors, or bomb."

    if move == "bomb" and bomb_used:
        return False, "Bomb can be used only once."

    return True, move


def resolve_round(user_move: str, bot_move: str):
    if user_move == "bomb" and bot_move == "bomb":
        return "draw"
    if user_move == "bomb":
        return "user"
    if bot_move == "bomb":
        return "bot"

    if user_move == bot_move:
        return "draw"

    wins = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper"
    }

    return "user" if wins[user_move] == bot_move else "bot"


def update_state(state: GameState, winner: str, user_move: str, bot_move: str):
    if user_move == "bomb":
        state.user_bomb_used = True
    if bot_move == "bomb":
        state.bot_bomb_used = True

    if winner == "user":
        state.user_score += 1
    elif winner == "bot":
        state.bot_score += 1

    if state.round_number == 3:
        state.game_over = True
    else:
        state.round_number += 1


def bot_move(state: GameState):
    moves = ["rock", "paper", "scissors"]
    if not state.bot_bomb_used:
        moves.append("bomb")
    return random.choice(moves)


def run_game():
    state = GameState()

    print(
        "Rock–Paper–Scissors–Plus\n"
        "Best of 3 rounds\n"
        "Moves: rock, paper, scissors, bomb\n"
        "Bomb beats all but can be used once\n"
    )

    while not state.game_over:
        print(f"\nRound {state.round_number}")
        user_input = input("Your move: ")

        valid, user_move = validate_move(user_input, state.user_bomb_used)
        bot_choice = bot_move(state)

        if not valid:
            print(user_move)
            print("Round wasted.")
            update_state(state, "draw", "invalid", bot_choice)
            continue

        if bot_choice == "bomb" and state.bot_bomb_used:
            bot_choice = random.choice(["rock", "paper", "scissors"])

        winner = resolve_round(user_move, bot_choice)
        update_state(state, winner, user_move, bot_choice)

        print(f"You played: {user_move}")
        print(f"Bot played: {bot_choice}")

        if winner == "draw":
            print("Result: Draw")
        elif winner == "user":
            print("Result: You win this round")
        else:
            print("Result: Bot wins this round")

        print(f"Score → You: {state.user_score}, Bot: {state.bot_score}")

    print("\nGame Over")
    if state.user_score > state.bot_score:
        print("Final Result: You win the game")
    elif state.bot_score > state.user_score:
        print("Final Result: Bot wins the game")
    else:
        print("Final Result: Draw")


if __name__ == "__main__":
    run_game()