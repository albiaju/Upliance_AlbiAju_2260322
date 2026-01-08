AI Game Referee – Rock–Paper–Scissors–Plus
=========================================

Overview
--------

This project implements a minimal AI referee for a Rock–Paper–Scissors–Plus game, designed to demonstrate agent-style reasoning, explicit state management, and tool-based game logic. The game runs in a simple CLI conversational loop and automatically ends after three rounds.

The focus is on correctness, clarity of state modeling, and clean separation between intent understanding, game logic, and response generation.

State Model
-----------

The game uses a single explicit state object (`GameState`) as the source of truth across turns. It tracks:

- Current round number (maximum 3)
- User and bot scores
- Whether each player has already used the bomb move
- Whether the game has ended

State is stored in Python code, not in prompts or implicit memory, ensuring deterministic behavior and preventing rule violations such as extra rounds or repeated bomb usage.

Agent and Tool Design
---------------------

The system follows a simple agent orchestration pattern:

1. Intent understanding
	- User input is interpreted and validated using a dedicated validation function.

2. Game logic
	- Core game rules (win/lose/draw resolution) are implemented as pure functions with no side effects.

3. State mutation tools
	- All updates to the game state (scores, round count, bomb usage) occur through a single state update function.

Key functions
-------------

- `validate_move` — checks input validity and enforces one-time bomb usage
- `resolve_round` — determines the round winner based on game rules
- `update_state` — mutates game state after each round

Tradeoffs
---------

The bot’s move selection uses simple randomness rather than strategy, to keep the focus on rule enforcement and state correctness.

The interface is CLI-based instead of graphical or web-based, as UI polish is out of scope for this assignment.

Future Improvements
-------------------

With more time, I would:

- Wrap the tools with explicit ADK schemas for structured inputs and outputs
- Add smarter bot strategies based on game history
- Introduce automated tests for edge cases
- Refactor the CLI loop into a reusable conversational runtime abstraction

How to run
----------

Run the game from the command line with:

```
python main.py
```

The CLI will prompt for moves. Valid moves are `rock`, `paper`, `scissors`, and `bomb` (bomb can be used once per player).

License
-------

This example is provided for educational purposes.
