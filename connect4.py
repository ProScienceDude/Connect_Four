import json
import os
from collections import defaultdict
import math # Import for infinity

# --- Game Constants ---
ROWS = 6
COLUMNS = 7
EMPTY = "-"
LEADERBOARD_FILE = "leader_board.txt"

# --- Board Functions (Unchanged) ---

def create_board():
    """Initializes a new Connect 4 board."""
    return [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board with column numbers."""
    for row in board:
        print(" ".join(row))
    print("-" * (COLUMNS * 2 - 1)) # Separator line
    print(" ".join([str(i) for i in range(COLUMNS)]))  # column numbers

def drop_piece(board, column, piece):
    """
    Drops a piece into the specified column.
    Returns True if successful, False if the column is full.
    """
    for row in reversed(board):
        if row[column] == EMPTY:
            row[column] = piece
            return True
    return False

def check_win(board, piece):
    """Checks for 4-in-a-row (horizontal, vertical, or diagonal) for the given piece."""
    # ... (Win logic is unchanged) ...
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    # Vertical check
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    # Diagonal (down-right)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    # Diagonal (up-right)
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False

def is_full(board):
    """Checks if the board is completely full (a draw state)."""
    return all(cell != EMPTY for row in board for cell in row)

# --- Leaderboard Functions (Updated) ---

def load_leaderboard():
    """Loads the leaderboard, adding 'min_turns' to the default structure."""
    
    # NEW DEFAULT STRUCTURE: 'min_turns' starts at float('inf')
    default_stats = {'wins': 0, 'games': 0, 'min_turns': float('inf')} 
    
    if not os.path.exists(LEADERBOARD_FILE):
        return defaultdict(lambda: default_stats.copy())
    
    try:
        with open(LEADERBOARD_FILE, 'r') as f:
            data = json.load(f)
            
            # Ensure loaded data has the 'min_turns' key, or default it.
            leaderboard = defaultdict(lambda: default_stats.copy())
            for player, stats in data.items():
                stats['min_turns'] = stats.get('min_turns', float('inf')) 
                leaderboard[player] = stats
                
            return leaderboard
    except (IOError, json.JSONDecodeError):
        print("Error reading leaderboard file. Starting with a fresh leaderboard.")
        return defaultdict(lambda: default_stats.copy())

def save_leaderboard(leaderboard):
    """Saves the current leaderboard to the file."""
    
    # Convert 'inf' to a string or a very large number for JSON serialization
    # Using a placeholder string "inf" for simplicity when writing to file.
    data_to_save = {}
    for player, stats in leaderboard.items():
        stats_copy = stats.copy()
        if stats_copy.get('min_turns', 0) == float('inf'):
             stats_copy['min_turns'] = "inf" # Use string for persistence
        data_to_save[player] = stats_copy

    try:
        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump(data_to_save, f, indent=4)
    except IOError:
        print("Error saving leaderboard to file.")

def update_leaderboard(leaderboard, winner, winning_turns, players):
    """Updates the game, win, and minimum turns counts for all participants."""
    
    for player_name in players:
        leaderboard[player_name]['games'] += 1
    
    if winner is not None:
        leaderboard[winner]['wins'] += 1
        
        # NEW LOGIC: Check if this is a new minimum turn count
        current_min = leaderboard[winner].get('min_turns', float('inf'))
        if winning_turns < current_min:
            leaderboard[winner]['min_turns'] = winning_turns
            
    save_leaderboard(leaderboard)

def display_leaderboard(leaderboard):
    """Prints the leaderboard sorted by win percentage and then total wins."""
    print("\n" + "="*50)
    print("      🏆 Connect 4 Leaderboard 🏆")
    print("="*50)
    
    # Prepare data for display and sorting
    prepared_players = []
    for name, stats in leaderboard.items():
        # Convert the string "inf" back to float('inf') for proper comparison
        min_turns = float(stats.get('min_turns', 'inf')) if isinstance(stats.get('min_turns'), str) else stats.get('min_turns', float('inf'))

        prepared_players.append({
            'name': name,
            'wins': stats['wins'],
            'games': stats['games'],
            'min_turns': min_turns,
            'win_percent': (stats['wins'] / stats['games'] if stats['games'] > 0 else 0)
        })

    # Sort by Win %, then Wins
    sorted_players = sorted(
        prepared_players, 
        key=lambda p: (p['win_percent'], p['wins']), 
        reverse=True
    )

    print(f"| {'Rank':<4} | {'Player':<15} | {'Wins':<5} | {'Games':<5} | {'Win %':<6} | {'Best Turn':<9} |")
    print("-" * 50)

    rank = 1
    for p in sorted_players:
        win_percent = f"{p['win_percent']:.2%}"
        
        # Display 'N/A' if min_turns is still infinity (no wins)
        best_turn_display = str(int(p['min_turns'])) if p['min_turns'] != float('inf') else "N/A"
        
        print(f"| {rank:<4} | {p['name']:<15} | {p['wins']:<5} | {p['games']:<5} | {win_percent:<6} | {best_turn_display:<9} |")
        rank += 1
    
    print("="*50 + "\n")


# --- Game Loop Functions (Updated) ---

def get_player_names():
    """Prompts the user for two player names."""
    print("👋 Welcome to Connect 4!")
    player1 = input("Player 1 (X), please enter your name: ").strip() or "Player 1"
    player2 = input("Player 2 (O), please enter your name: ").strip() or "Player 2"
    if player1.upper() == player2.upper():
        print("Names are too similar! Appending ' (2)' to the second player.")
        player2 = player2 + " (2)"

    print(f"\nGame Start: {player1} (X) vs {player2} (O)\n")
    return player1, player2

def play_game(player_names, leaderboard):
    """The core Connect 4 game loop."""
    p1_name, p2_name = player_names
    board = create_board()
    turn = 0 # Turn counter (starts at 0)
    game_over = False
    winner_name = None
    winning_turns = None

    print_board(board)

    while not game_over:
        piece = "X" if turn % 2 == 0 else "O"
        current_player_name = p1_name if piece == "X" else p2_name
        
        try:
            column = int(input(f"{current_player_name} ({piece}), choose a column (0-{COLUMNS-1}): "))
            if not (0 <= column < COLUMNS):
                print("⚠️ Invalid column. Please choose a number within the board range.")
                continue
        except ValueError:
            print("❌ Invalid input. Please enter a numerical column index.")
            continue

        if not drop_piece(board, column, piece):
            print("✋ Column full. Try a different one.")
            continue
        
        # Turn is incremented AFTER a piece is successfully dropped
        turn += 1

        print_board(board)

        if check_win(board, piece):
            print(f"🎉 {current_player_name} ({piece}) wins in {turn} turns! Congratulations!")
            winner_name = current_player_name
            winning_turns = turn # Record the number of turns
            game_over = True
        elif is_full(board):
            print("🤝 It's a draw!")
            game_over = True
        # If no win/draw, loop continues and turn is already incremented
    
    # Update and save the leaderboard after the game ends
    # Pass the total number of turns
    update_leaderboard(leaderboard, winner_name, winning_turns, player_names)


def main_menu():
    """Manages the game menu and state."""
    leaderboard = load_leaderboard()
    p1_name, p2_name = get_player_names()
    
    while True:
        print("\n" + "="*25)
        print("      Connect 4 Menu")
        print("="*25)
        print("1. ▶️ Play Game")
        print("2. 🏆 View Leaderboard")
        print("3. 🚪 End Game")
        print("="*25)
        
        choice = input("Enter your choice (1, 2, or 3): ").strip()
        
        if choice == '1':
            play_game((p1_name, p2_name), leaderboard)
        elif choice == '2':
            display_leaderboard(leaderboard)
        elif choice == '3':
            print(f"\nThanks for playing, {p1_name} and {p2_name}! Goodbye. 👋")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# --- Program Entry Point ---
if __name__ == "__main__":
    main_menu()