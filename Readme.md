# AI Game Referee – Rock–Paper–Scissors–Plus

## Role
AI Product Engineer (Conversational Agents)

## Language
Python

## Framework / SDK
Google ADK (agent + tools pattern)

## Interface
CLI-based conversational loop

---

## Overview

This project implements a minimal AI referee for a Rock–Paper–Scissors–Plus game. The goal is to demonstrate agent-oriented design using explicit state management, tool-based logic, and deterministic control flow, aligned with Google ADK principles.

The game runs for a maximum of three rounds, validates user input, enforces constraints such as one-time bomb usage, and terminates automatically with a clear final result.

---

## State Model

The system uses a single explicit state object (`GameState`) that persists across turns. This state acts as the single source of truth and is never stored in prompts or inferred implicitly.

The state tracks:

- **Current round number** (maximum of 3)
- **User score and bot score**
- **Whether the bomb move has been used** by each player
- **Whether the game has ended**

By externalizing state in code, the agent remains deterministic and resistant to prompt-based inconsistencies.

---

## Agent and Tool Design

The implementation follows a clear agent–tool separation inspired by Google ADK:

### Agent (Control Loop)

The main game loop acts as the agent:

- Receives user input
- Determines which tool to call
- Controls turn progression
- Enforces termination after three rounds

### Tools (Explicit Functions)

Core logic is encapsulated in dedicated tools:

- **`validate_move`** — interprets user intent and enforces input constraints
- **`resolve_round`** — applies game rules to decide the round winner
- **`update_state`** — mutates game state (scores, rounds, bomb usage)
- **`bot_move`** — selects a random move for the bot

Each tool has a single responsibility, making the system easy to reason about and extend.

---

## Response Generation

User-facing responses are generated separately from logic, ensuring that explanation does not interfere with rule enforcement.

---

## Game Rules

- **Standard moves**: rock, paper, scissors (standard RPS rules apply)
- **Bomb move**: Beats all other moves but can only be used once per player
- **Best of 3**: The game ends after three rounds; highest score wins

### Round Outcomes

- If both players play bomb → Draw
- If one player plays bomb → Bomb player wins
- If both play the same standard move → Draw
- Otherwise → Standard RPS rules apply (rock beats scissors, scissors beats paper, paper beats rock)

---

## Tradeoffs

- The bot's move selection is intentionally random rather than strategic, keeping the focus on agent correctness and rule enforcement.
- The interface is CLI-based, as UI and frontend concerns are out of scope for this assignment.
- Google ADK concepts are applied architecturally rather than through heavy SDK-specific imports.

---

## Future Improvements

With more time, the system could be enhanced by:

- Adding explicit ADK schemas or JSON-structured tool outputs
- Implementing adaptive bot strategies based on game history
- Introducing automated tests for edge cases
- Abstracting the conversational loop into a reusable agent runtime
- Persisting game history and statistics

---

## How to Run

```bash
python main.py
```

Follow the on-screen prompts to play the game. Enter your move (rock, paper, scissors, or bomb) for each round.

---

## Project Structure

```
.
├── main.py          # Core game implementation
└── README.md        # This file
```

---

## Example Gameplay

```
Rock–Paper–Scissors–Plus
Best of 3 rounds
Moves: rock, paper, scissors, bomb
Bomb beats all but can be used once

Round 1
Your move: rock
You played: rock
Bot played: scissors
Result: You win this round
Score → You: 1, Bot: 0

Round 2
Your move: paper
You played: paper
Bot played: paper
Result: Draw
Score → You: 1, Bot: 0

Round 3
Your move: bomb
You played: bomb
Bot played: rock
Result: You win this round
Score → You: 2, Bot: 0

Game Over
Final Result: You win the game
```

---

## Design Philosophy

This implementation prioritizes:

1. **Explicit State Management** — All game state is centralized in a `GameState` object
2. **Separation of Concerns** — Logic is split into focused, single-responsibility tools
3. **Deterministic Behavior** — Rules are enforced consistently, independent of user input
4. **Clarity Over Complexity** — Code is readable and maintainable, not over-engineered
5. **Agent-Oriented Architecture** — Following Google ADK patterns for future scalability

---
## Python Implementation

### File: main.py

```python
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
```



