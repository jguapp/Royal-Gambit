# Royal Gambit ♞♛

**Royal Gambit** is an interactive chess game built in Python using Pygame. It features an AI powered by a minimax algorithm, a dynamic GUI with animated backgrounds and sound effects, and comprehensive move validation including special moves like castling, en passant, and pawn promotion.

## Features ✨

- **Interactive Gameplay:**  
  Drag-and-drop pieces and a dedicated move log for easy tracking.

- **Intelligent AI Opponent:**  
  Uses a minimax algorithm with alpha-beta pruning to evaluate hundreds of book moves.

- **Comprehensive Move Validation:**  
  Full support for castling, en passant, and pawn promotion.

- **Customizable Options:**  
  Change themes on the fly and easily switch back to the main menu at any time.

## Installation 💾

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/jguapp/AI-Chess-Bot.git
   cd AI-Chess-Bot
   ```

2. **Set Up a Virtual Environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Game:**

   ```bash
   python main.py
   ```

## Usage 🎮

- **Start Menu:**  
  Use the main menu to start a new game, play against the AI, or view instructions.  
  - Press **ESC** anytime during the difficulty selection screen to return to the main menu.

- **In-Game Controls:**  
  - **Drag-and-drop** pieces for an interactive experience.
  - Press **T** to change the theme, **R** to reset the game, and **ESC** to return to the menu.

## Roadmap 🚀

- **Online Multiplayer:**  
  Enable real-time games with opponents worldwide.
- **Enhanced AI**
  Improve decision-making speed and move quality using advanced heuristics and machine learning.
- **Custom Themes, Tutorials, and more Game Modes**
  Add more board/piece themes and in-game tutorials for beginners.
