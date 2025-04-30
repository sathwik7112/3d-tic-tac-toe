document.addEventListener('DOMContentLoaded', () => {
  console.log("🎮 FourSight 3D Tic Tac Toe initialized");
  
  // DOM Elements
  const statusEl = document.getElementById('status');
  const diffBtns = document.querySelectorAll('.diff-btn');
  const restartBtn = document.getElementById('restart');
  const rulesBtn = document.getElementById('rules');
  const cells = document.querySelectorAll('.cell');
  const modal = document.getElementById('rules-modal');
  const closeModal = document.querySelector('.close-modal');
  const depthStat = document.getElementById('depth-stat');
  const timeStat = document.getElementById('time-stat');
  const playerToken = document.querySelector('.player-token');
  
  // Game variables
  let depth = 0;
  let board;
  let gameOver;
  let activeDiffBtn = null;
  
  // Sound effects (uncomment if you want to add sounds)
  /*
  const sounds = {
    click: new Audio('/static/sounds/click.mp3'),
    win: new Audio('/static/sounds/win.mp3'),
    lose: new Audio('/static/sounds/lose.mp3'),
    draw: new Audio('/static/sounds/draw.mp3'),
    move: new Audio('/static/sounds/move.mp3')
  };
  */
  
  // Initialize game
  function initGame() {
    // Create empty 4x4x4 board
    board = Array(4).fill().map(() => 
      Array(4).fill().map(() => Array(4).fill('.'))
    );
    
    gameOver = false;
    
    // Reset cells
    cells.forEach(cell => {
      cell.textContent = '';
      cell.disabled = false;
      cell.removeAttribute('data-content');
      cell.classList.remove('win-x', 'win-o');
    });
    
    // Reset stats
    depthStat.textContent = '-';
    timeStat.textContent = '-';
    
    // Update status message
    statusEl.textContent = depth 
      ? 'YOUR MOVE (X)'
      : 'SELECT DIFFICULTY TO START';
      
    // Add animation
    statusEl.classList.add('pulse');
    setTimeout(() => statusEl.classList.remove('pulse'), 500);
    
    // Make sure player token shows X
    playerToken.textContent = 'X';
  }
  
  // Set difficulty
  function setDifficulty(btn) {
    // Remove active class from previous button
    if (activeDiffBtn) {
      activeDiffBtn.classList.remove('active');
    }
    
    // Set new active button
    btn.classList.add('active');
    activeDiffBtn = btn;
    
    // Play sound
    // sounds.click.play();
    
    // Get difficulty value
    depth = parseInt(btn.dataset.value, 10);
    console.log(`Difficulty set to: ${depth}`);
    
    // Reset game with new difficulty
    initGame();
  }
  
  // Handle cell click
  async function handleCellClick(cell) {
    if (gameOver || !depth) return;
    
    // Play sound
    // sounds.click.play();
    
    console.log(`Cell clicked: ${cell.dataset.pos}`);
    
    // Get cell coordinates
    const [z, y, x] = cell.dataset.pos.split(',').map(Number);
    
    // Make human move
    board[z][y][x] = 'X';
    cell.textContent = 'X';
    cell.setAttribute('data-content', 'X');
    cell.disabled = true;
    
    // Add animation
    cell.classList.add('pulse');
    setTimeout(() => cell.classList.remove('pulse'), 300);
    
    // Show loading state
    statusEl.innerHTML = 'AI THINKING<span class="dots">...</span>';
    addLoadingAnimation();
    
    // Check for human win or draw
    try {
      const statusResp = await fetch('/check_status', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ board })
      });
      
      const statusData = await statusResp.json();
      
      if (statusData.winner) {
        // Human wins
        if (statusData.line) {
          highlightWinningLine('X', statusData.line);
        }
        // sounds.win.play();
        return endGame('X');
      }
      
      if (statusData.draw) {
        // Draw game
        // sounds.draw.play();
        return endGame('draw');
      }
      
      // AI turn
      const t0 = performance.now();
      
      const aiResp = await fetch('/ai_move', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ board, depth })
      });
      
      const aiData = await aiResp.json();
      const t1 = performance.now();
      
      // Update stats
      if (aiData.depth_reached) {
        depthStat.textContent = aiData.depth_reached;
      }
      
      if (aiData.time_taken) {
        timeStat.textContent = `${aiData.time_taken.toFixed(2)}s`;
      } else {
        timeStat.textContent = `${((t1 - t0) / 1000).toFixed(2)}s`;
      }
      
      // Update board from AI response
      board = aiData.board;
      
      // Apply AI move with delay for better UX
      if (aiData.move) {
        const [az, ay, ax] = aiData.move;
        const aiCell = document.querySelector(`.cell[data-pos="${az},${ay},${ax}"]`);
        
        setTimeout(() => {
          // sounds.move.play();
          aiCell.textContent = 'O';
          aiCell.setAttribute('data-content', 'O');
          aiCell.disabled = true;
          
          // Add animation
          aiCell.classList.add('pulse');
          setTimeout(() => aiCell.classList.remove('pulse'), 300);
          
          // Check for AI win or draw
          if (aiData.winner) {
            if (aiData.line) {
              highlightWinningLine('O', aiData.line);
            }
            // sounds.lose.play();
            setTimeout(() => endGame('O'), 500);
            return;
          }
          
          if (aiData.draw) {
            // sounds.draw.play();
            setTimeout(() => endGame('draw'), 500);
            return;
          }
          
          // Continue game - human's turn
          statusEl.textContent = 'YOUR MOVE (X)';
        }, 400); // Short delay for better UX
      }
      
    } catch (error) {
      console.error("Error during game:", error);
      statusEl.textContent = 'ERROR - PLEASE RESTART';
    }
  }
  
  // Add loading animation to status
  function addLoadingAnimation() {
    const dots = document.querySelector('.dots');
    if (!dots) return;
    
    let count = 0;
    const interval = setInterval(() => {
      count = (count + 1) % 4;
      dots.textContent = '.'.repeat(count);
      
      // Clear interval when status no longer has dots
      if (!document.querySelector('.dots')) {
        clearInterval(interval);
      }
    }, 300);
  }
  
  // Highlight winning line
  function highlightWinningLine(player, line) {
    if (!line) return;
    
    const className = player === 'X' ? 'win-x' : 'win-o';
    
    for (const [z, y, x] of line) {
      const cell = document.querySelector(`.cell[data-pos="${z},${y},${x}"]`);
      if (cell) {
        cell.classList.add(className);
      }
    }
  }
  
  // End game
  function endGame(result) {
    gameOver = true;
    let message = '';
    
    if (result === 'X') {
      message = '🎉 YOU WIN!';
      statusEl.style.color = '#00a2ff';
    } else if (result === 'O') {
      message = '💻 AI WINS!';
      statusEl.style.color = '#ff3366';
    } else {
      message = "🔄 IT'S A DRAW!";
      statusEl.style.color = '#ffcc00';
    }
    
    statusEl.textContent = message;
    cells.forEach(cell => cell.disabled = true);
    
    // Add winning animation
    statusEl.classList.add('pulse');
    setTimeout(() => {
      statusEl.classList.remove('pulse');
      // Reset color after animation
      setTimeout(() => statusEl.style.color = '', 2000);
    }, 1000);
  }
  
  // Event Listeners
  
  // Difficulty buttons
  diffBtns.forEach(btn => {
    btn.addEventListener('click', () => setDifficulty(btn));
  });
  
  // Cell clicks
  cells.forEach(cell => {
    cell.addEventListener('click', () => handleCellClick(cell));
  });
  
  // Restart button
  restartBtn.addEventListener('click', () => {
    // sounds.click.play();
    initGame();
  });
  
  // Rules button
  rulesBtn.addEventListener('click', () => {
    // sounds.click.play();
    modal.style.display = 'flex';
    
    // Fade in effect
    modal.style.opacity = 0;
    setTimeout(() => {
      modal.style.opacity = 1;
    }, 10);
  });
  
  // Close modal
  closeModal.addEventListener('click', () => {
    // sounds.click.play();
    modal.style.opacity = 0;
    setTimeout(() => {
      modal.style.display = 'none';
    }, 300);
  });
  
  // Close modal by clicking outside
  window.addEventListener('click', (event) => {
    if (event.target === modal) {
      modal.style.opacity = 0;
      setTimeout(() => {
        modal.style.display = 'none';
      }, 300);
    }
  });
  
  // Add extra CSS for animations
  const style = document.createElement('style');
  style.textContent = `
    @keyframes glow {
      0% { box-shadow: 0 0 5px rgba(57, 255, 20, 0.5); }
      50% { box-shadow: 0 0 15px rgba(57, 255, 20, 0.8); }
      100% { box-shadow: 0 0 5px rgba(57, 255, 20, 0.5); }
    }
    
    .board:hover {
      animation: glow 2s infinite;
    }
    
    .dots {
      display: inline-block;
      width: 20px;
      text-align: left;
    }
    
    .modal {
      transition: opacity 0.3s ease;
    }
  `;
  document.head.appendChild(style);
  
  // Initialize game
  initGame();
});