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
Create & activate a virtual environment (optional)

bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # Unix/macOS
venv\Scripts\activate      # Windows
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Usage
Select Difficulty: Click Easy, Difficult, or Insane.

Make a Move: Click an empty slot to place an 'X'.

AI Response: Wait for the AI to compute its 'O' move (up to 5 seconds).

Game Status: Monitor win, lose, or draw messages and move stats.

Reset: Click RESET to start a new game.

How to Run
Create a project folder on your local machine (e.g., on Desktop).

Open VS Code, and in the terminal navigate into that folder:

bash
Copy
Edit
cd ~/Desktop/project-2
Clone this repo into the folder:

bash
Copy
Edit
git clone <repository-url> .
Install Flask (if not already installed):

bash
Copy
Edit
pip3 install flask
Start the backend server:

bash
Copy
Edit
python3 backend/app.py
Make sure your terminal’s working directory is the project root—the one containing backend/.

Open the game: In your browser, go to the URL printed in the terminal, for example:

csharp
Copy
Edit
* Running on http://127.0.0.1:5000
Enjoy playing—click the link and start your 3D Tic-Tac-Toe match!

Project Structure
text
Copy
Edit
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
Contributors
Esha Santhoshini Pothukanuru

Rishik Kasula

Sai Keerthan Bingi

Sai Vishnu Sathwik Gurijala

License
This project is released under the MIT License. See LICENSE for details.
