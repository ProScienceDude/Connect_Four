import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tkinter as tk
from tkinter import messagebox
import os
from collections import defaultdict

# --- Setup for Tkinter Popups (Needed for cross-platform dialogs) ---
# Initialize Tkinter and hide the main window
try:
    ROOT = tk.Tk()
    ROOT.withdraw() 
except Exception:
    # Handle cases where tkinter might not be available
    print("Warning: Tkinter is not fully initialized. Popups will use basic console print.")
    ROOT = None

# --- Game Constants ---
ROWS = 6
COLUMNS = 7
EMPTY = 0
PIECE_X = 1 # Player X (Red)
PIECE_O = 2 # Player O (Yellow)
PIECE_COLORS = {PIECE_X: 'red', PIECE_O: 'yellow'}
PIECE_NAMES = {PIECE_X: 'Player X', PIECE_O: 'Player O'}
LEADERBOARD_FILE = "connect4_leaderboard.txt"

# --- Game State ---
board = []
current_player = PIECE_X
game_over = False
move_count = 0
player_names = {PIECE_X: "Player 1", PIECE_O: "Player 2"}

# --- Core Game Logic ---

def create_board():
    """Initializes and returns an empty Connect 4 board."""
    return [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]

def get_available_row(board, col):
    """Finds the lowest empty row index in a given column."""
    for r in range(ROWS):
        if board[r][col] == EMPTY:
            return r
    return None  # Column is full

def drop_piece(board, row, col, piece):
    """Places a piece at the specified row and column."""
    board[row][col] = piece

def check_win(board, piece):
    """Checks if the given piece has won the game (4 in a row)."""
    # Helper to check if a sequence of 4 coordinates (r, c) contains only the target piece
    def check_sequence(coords):
        return all(board[r][c] == piece for r, c in coords)

    # 1. Check Horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if check_sequence([(r, c+i) for i in range(4)]): return True

    # 2. Check Vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if check_sequence([(r+i, c) for i in range(4)]): return True

    # 3. Check Diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if check_sequence([(r+i, c+i) for i in range(4)]): return True

    # 4. Check Diagonal (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if check_sequence([(r-i, c+i) for i in range(4)]): return True

    return False

def is_full(board):
    """Checks if the board is completely full (a draw condition)."""
    return all(board[ROWS - 1][c] != EMPTY for c in range(COLUMNS))

# --- Leaderboard Logic (File I/O) ---

def moves_file(winner_name=None, winning_moves=None, show_only=False):
    """
    Handles reading, updating, and displaying the leaderboard.
    Scores are based on the minimum number of moves to win.
    """
    leaderboard = defaultdict(lambda: float('inf'))

    # 1. Read existing leaderboard data
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as f:
                for line in f:
                    line = line.strip()
                    if ':' in line:
                        try:
                            name, move_str = line.split(":", 1)
                            leaderboard[name.strip()] = min(float(move_str.strip()), leaderboard[name.strip()])
                        except ValueError:
                            continue # Skip corrupted lines
        except Exception as e:
            print(f"Error reading leaderboard file: {e}")

    # 2. Update with new win, if provided and better
    if winner_name and winning_moves is not None:
        if winning_moves < leaderboard[winner_name]:
            leaderboard[winner_name] = winning_moves
            print(f"\nLeaderboard Updated: {winner_name} set a new record with {winning_moves} moves!")

    # 3. Sort by moves (ascending) and prepare for display/write
    # Filter out entries where moves is still 'inf' (shouldn't happen, but safe)
    sorted_moves = {k: v for k, v in leaderboard.items() if v != float('inf')}
    sorted_moves = dict(sorted(sorted_moves.items(), key=lambda item: item[1]))

    # 4. Write updated and sorted leaderboard back to file (if not show_only)
    if winner_name or not show_only:
        try:
            with open(LEADERBOARD_FILE, "w") as f:
                for name, move in sorted_moves.items():
                    f.write(f"{name}: {move:.2f}\n")
        except Exception as e:
            print(f"Error writing to leaderboard file: {e}")

    # 5. Display Leaderboard in the console
    print("\n" + "="*40)
    print("       🏆 Connect 4 Leaderboard 🏆")
    print(" (Least Moves to Win - File: leaderboard.txt)")
    print("="*40)
    if not sorted_moves:
        print("No wins recorded yet!")
    else:
        for rank, (name, move) in enumerate(sorted_moves.items(), 1):
            display_move = int(move) if move == int(move) else f"{move:.2f}"
            print(f"{rank}. {name}: {display_move} moves")
    print("="*40)

# --- Matplotlib UI Logic ---

def draw_board():
    """Draws the Connect 4 board and pieces using Matplotlib."""
    ax.clear()
    ax.set_xlim(0, COLUMNS)
    ax.set_ylim(0, ROWS)
    ax.set_aspect('equal')
    plt.axis('off')
    
    # Draw the main blue Connect Four grid
    ax.add_patch(patches.Rectangle((0, 0), COLUMNS, ROWS, facecolor='#0d47a1', edgecolor='none'))

    # Draw the holes and pieces
    for r in range(ROWS):
        for c in range(COLUMNS):
            # Draw empty hole circle
            hole = patches.Circle((c + 0.5, r + 0.5), 0.45, color='white')
            ax.add_patch(hole)

            piece = board[r][c]
            if piece != EMPTY:
                # Draw the piece over the hole
                color = PIECE_COLORS[piece]
                ax.add_patch(patches.Circle((c + 0.5, r + 0.5), 0.4, color=color, zorder=10))

    # Add a thin gray line to separate clickable areas (optional, for guidance)
    for c in range(1, COLUMNS):
        ax.plot([c, c], [0, ROWS], 'k-', lw=0.5, alpha=0.3)

    plt.title(f"Current Turn: {player_names[current_player]} ({'X' if current_player == PIECE_X else 'O'})")
    plt.draw()

def on_click(event):
    """Handles mouse click events for dropping a piece."""
    global current_player, game_over, move_count

    if game_over or event.xdata is None or event.ydata is None:
        return

    # Determine the column clicked
    col = int(event.xdata)
    if col < 0 or col >= COLUMNS:
        return

    row = get_available_row(board, col)

    if row is not None:
        drop_piece(board, row, col, current_player)
        move_count += 1
        
        # Check game status
        if check_win(board, current_player):
            winner_name = player_names[current_player]
            winning_moves = (move_count + 1) // 2
            game_over = True
            
            # Update leaderboard and show result/menu
            moves_file(winner_name, winning_moves)
            
            # Use Tkinter popup for game end menu
            show_game_end_menu(f"🎉 {winner_name} wins in {winning_moves} moves! 🎉")
            
        elif is_full(board):
            game_over = True
            show_game_end_menu("🤝 It's a draw! 🤝")
            
        else:
            # Switch player
            current_player = PIECE_O if current_player == PIECE_X else PIECE_X
            draw_board() # Redraw board for new turn indicator

    else:
        # Console message for column full, since Matplotlib doesn't have easy temporary UI messages
        print("Column is full! Try a different one.")

# --- Post-Game Menu/Popup Logic ---

def show_game_end_menu(message):
    """
    Displays the post-game menu using Tkinter's message box (if available).
    """
    if ROOT:
        # Custom button names are not possible, so we use a prompt that maps
        # Yes -> Replay, No -> Leaderboard, Cancel -> Quit
        response = messagebox.askyesnocancel(
            "Game Over! What's next?",
            f"{message}\n\nDo you want to **REPLAY**?\n\n- Press 'Yes' to Replay\n- Press 'No' to View Leaderboard\n- Press 'Cancel' to Quit"
        )
        
        if response is True:
            reset_game()
        elif response is False:
            moves_file(show_only=True)
            # After showing console leaderboard, ask again
            show_game_end_menu(message) 
        else: # response is None (Cancel)
            plt.close(fig) # Close the Matplotlib figure
            print("\nThanks for playing! Goodbye.")
    else:
        # Fallback for environments without Tkinter UI
        print(f"\n--- {message} ---")
        moves_file(show_only=True)
        choice = input("Enter 'R' to Replay or 'Q' to Quit: ").strip().upper()
        if choice == 'R':
            reset_game()
        else:
            plt.close(fig)
            print("\nThanks for playing! Goodbye.")
            
def reset_game():
    """Resets the game state and redraws the board."""
    global board, current_player, game_over, move_count
    
    # Reset state
    board = create_board()
    current_player = PIECE_X
    game_over = False
    move_count = 0
    
    # Redraw
    draw_board()
    print("\n--- New Game Started ---")

# --- Main Application Setup ---

if __name__ == '__main__':
    # Get player names from console before starting the UI
    print("Welcome to Connect Four!")
    try:
        name_x = input("Enter name for Player X (Red): ").strip()
        name_o = input("Enter name for Player O (Yellow): ").strip()
        player_names[PIECE_X] = name_x if name_x else "Player 1"
        player_names[PIECE_O] = name_o if name_o else "Player 2"
    except EOFError:
        print("Using default player names.")
        
    # Initial leaderboard display
    moves_file(show_only=True)

    # Initialize Matplotlib Figure and Axis
    fig, ax = plt.subplots(figsize=(COLUMNS, ROWS))
    fig.canvas.manager.set_window_title('Connect Four')

    # Connect click event handler
    fig.canvas.mpl_connect('button_press_event', on_click)
    
    # Initial setup
    reset_game() 

    # Show the plot and start the event loop
    plt.show()

