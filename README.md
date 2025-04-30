# 3D Tic-Tac-Toe

A one-player, 4×4×4 Tic-Tac-Toe game with an AI opponent implemented using the Mini-Max algorithm with Alpha–Beta pruning and a 5-second search cutoff. Difficulty levels control search depth: Easy (2 plies), Difficult (4 plies), Insane (6 plies).

---

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

---

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

2. **Create & activate a virtual environment** (optional)
   ```bash
   python -m venv venv
   source venv/bin/activate   # Unix/macOS
   venv\Scripts\activate    # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open your browser**
   Visit `http://localhost:5000` to play the game.

---

## Project Structure

```text
project-root/
├─ app.py                # Flask server and route handlers
├─ game_logic.py         # Board setup, Mini-Max & Alpha–Beta AI logic
├─ requirements.txt      # Python dependencies
├─ templates/
│  └─ index.html         # Main HTML layout and UI
└─ static/
   ├─ css/
   │  └─ style.css       # Retro terminal–style UI
   └─ js/
      └─ app.js          # Frontend interactivity & API calls
```

---

## Usage

1. **Select Difficulty**: Click Easy, Difficult, or Insane.
2. **Make a Move**: Click an empty slot to place an 'X'.
3. **AI Response**: Wait for the AI to compute its 'O' move (up to 5 seconds).
4. **Game Status**: Monitor win, lose, or draw messages and move stats.
5. **Reset**: Click **RESET** to start a new game.

---

## Contributors

- Esha Santhoshini Pothukanuru  
- Rishik Kasula  
- Sai Keerthan Bingi  
- Sai Vishnu Sathwik Gurijala  

---

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.
