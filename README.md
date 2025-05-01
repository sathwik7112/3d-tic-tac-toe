# 3D Tic-Tac-Toe

A one-player, 4×4×4 Tic-Tac-Toe game with an AI opponent implemented using the Mini-Max algorithm with Alpha–Beta pruning and a 5-second search cutoff. Difficulty levels control search depth: Easy (2 plies), Difficult (4 plies), Insane (6 plies).

## Features

- **3D Board**: Four 4×4 layers (64 slots) displayed in a retro terminal style UI.
- **AI Opponent**: Uses iterative deepening with Alpha–Beta pruning for efficient search.
- **Difficulty Levels**:
  - Easy: Depth = 2 plies
  - Difficult: Depth = 4 plies
  - Insane: Depth = 6 plies
- **Time Cutoff**: AI search stops after 5 seconds to ensure responsiveness.
- **Client–Server Architecture**:
  - **Backend**: Flask (Python) REST API for game logic and AI moves.
  - **Frontend**: HTML/CSS/JavaScript for interactive UI and game controls.

## Demo

[View Live Demo](http://127.0.0.1:5000) (When running locally)

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- Virtual environment tool (optional but recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Create & activate a virtual environment (optional)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Unix/macOS
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Select Difficulty**: Click Easy, Difficult, or Insane.
2. **Make a Move**: Click an empty slot to place an 'X'.
3. **AI Response**: Wait for the AI to compute its 'O' move (up to 5 seconds).
4. **Game Status**: Monitor win, lose, or draw messages and move stats.
5. **Reset**: Click RESET to start a new game.

## How to Run

1. Create a project folder on your local machine (e.g., on Desktop).
2. Open VS Code, and in the terminal navigate into that folder:
   ```bash
   cd ~/Desktop/project-2
   ```
3. Clone this repo into the folder:
   ```bash
   git clone <repository-url> .
   ```
4. Install Flask (if not already installed):
   ```bash
   pip3 install flask
   ```
5. Start the backend server:
   ```bash
   python3 backend/app.py
   ```
   Make sure your terminal's working directory is the project root—the one containing backend/.
6. Open the game: In your browser, go to the URL printed in the terminal, for example:
   ```
   * Running on http://127.0.0.1:5000
   ```
7. Enjoy playing—click the link and start your 3D Tic-Tac-Toe match!

## Project Structure

```
project-root/
├─ backend/
│  ├─ app.py              # Flask server and route handlers
│  └─ game_logic.py       # Board setup, Mini-Max & Alpha–Beta AI logic
├─ static/
│  ├─ css/
│  │  └─ style.css        # Retro terminal–style UI
│  └─ js/
│     └─ app.js          # Frontend interactivity & API calls
├─ templates/
│  └─ index.html          # Main HTML layout and UI
└─ requirements.txt       # Python dependencies
```

## Technical Implementation

- **AI Algorithm**: The computer opponent uses the Mini-Max algorithm with Alpha-Beta pruning to efficiently search for optimal moves.
- **Search Optimization**: Iterative deepening is employed to ensure the AI can return a move within the 5-second time limit.
- **Win Detection**: Algorithms to detect winning conditions across rows, columns, and all 3D diagonals.
- **RESTful API**: Backend Flask server provides endpoints for game state management and AI move calculation.

## Contributors

- Esha Santhoshini Pothukanuru
- Rishik Kasula
- Sai Keerthan Bingi
- Sai Vishnu Sathwik Gurijala

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

- Thanks to all who provided feedback during testing
- Inspiration from classic Tic-Tac-Toe games
