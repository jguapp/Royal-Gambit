<div align="center">

# Royal Gambit ♞

**A complete chess board, a stubborn AI, and no browser required.**

Play locally or challenge a computer opponent that opens from a real move book,
then switches to minimax with alpha-beta pruning when the position leaves theory.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-2C2D72?style=for-the-badge&logo=python&logoColor=white)

</div>

---

## What it is

Royal Gambit is a desktop chess game written in Python and rendered with
Pygame. It supports local two-player games and four AI difficulty levels in a
single interface with drag-and-drop pieces, move highlighting, sound, themes,
and a running move log.

The chess logic is implemented in the project itself. Legal moves, turns,
captures, checks, checkmate, castling, en passant, and promotion are handled by
the board model rather than delegated to an external chess engine.

## The opponent

The AI begins with a weighted opening book. Once the game leaves a known line,
it searches future positions with minimax and alpha-beta pruning.

Its evaluation combines:

- Material balance
- Piece-square heat maps
- Mobility
- Captures and king threats
- Difficulty-dependent search depth

| Difficulty | Search depth |
|---|---:|
| Easy | 2 plies |
| Medium | 4 plies |
| Hard | 6 plies |
| Expert | 8 plies |

## Features

| | |
|---|---|
| **Two game modes** | Local two-player or player versus AI |
| **Complete rules** | Castling, en passant, promotion, check, and checkmate |
| **Direct manipulation** | Drag pieces, preview legal squares, and inspect the previous move |
| **Opening theory** | Weighted book moves before minimax takes over |
| **Ten board themes** | Green, brown, blue, purple, red, yellow, orange, pink, cyan, and teal |
| **Game feedback** | Move log, hover states, end-game messages, and distinct sounds |

## Controls

| Input | Action |
|---|---|
| Drag and drop | Move a piece |
| **T** | Change the board theme |
| **R** | Reset the game |
| **Esc** | Return to the main menu |

## Run it

```bash
git clone https://github.com/jguapp/Royal-Gambit.git
cd Royal-Gambit/ai_chess_bot

python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install pygame
python src/main.py
```

Python 3.10 or newer is recommended.

## Project structure

```text
ai_chess_bot/
├── assets/            piece art, sounds, and animated menu background
└── src/
    ├── ai.py          opening book, evaluation, minimax, alpha-beta pruning
    ├── board.py       board state and legal move generation
    ├── game.py        turns, UI state, move log, and end-game handling
    ├── main.py        application loop and input
    ├── menu.py        start menu, controls, and difficulty selection
    └── piece.py       piece models and movement rules
```

## Status

Royal Gambit is a working portfolio project. The strongest next steps are
automated move-generation tests, position import/export, and online multiplayer.

---

<div align="center">
Built by <a href="https://github.com/jguapp">Joel Vasquez</a>
</div>

