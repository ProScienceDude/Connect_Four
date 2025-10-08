ROWS = 6
COLUMNS = 7
EMPTY = "-"

# --- Board Management ---

# Creating board
def create_board():
    """Initializes and returns an empty Connect 4 board."""
    return [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]

def get_available_row(board, column):
    """Finds the next available row index for a given column, or None if full."""
    for r in range(ROWS):
        if board[r][column] == EMPTY:
            return r
    return None

# Dropping piece
def drop_piece_at(board, row, column, piece):
    """Places a piece ('X' or 'O') at the specified row and column."""
    if 0 <= row < ROWS and 0 <= column < COLUMNS:
        board[row][column] = piece
        return True
    return False

# Checking if board is full
def is_full(board):
    """Checks if the entire board is filled with pieces."""
    return all(cell != EMPTY for row in board for cell in row)

# --- Win Condition ---

# Checking win condition
def check_win(board, piece):
    """Checks if the given piece has achieved four in a row (horizontal, vertical, or diagonal)."""
    # Horizontal Check
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    # Vertical Check
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    # Diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    # Diagonal (top-left to bottom-right)
    # The original file's comment was 'Diagonal upar-left' but the code checks bottom-left to top-right visually on a standard array representation
    # Correcting the range to match the logic: starts from row 3 (r=3) and goes down (r-i) as c goes up (c+i)
    for r in range(3, ROWS): 
        for c in range(COLUMNS - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     game_board = create_board()
#     print("Empty Board:")
#     for row in game_board:
#         print(row)
    
#     # Drop some pieces to test
#     drop_piece_at(game_board, 0, 0, "X")
#     drop_piece_at(game_board, 1, 0, "X")
#     drop_piece_at(game_board, 2, 0, "X")
#     drop_piece_at(game_board, 3, 0, "X") # X should win vertically

#     print("\nBoard after moves:")
#     for row in game_board:
#         print(row)
        
#     print(f"\nWin check for X: {check_win(game_board, 'X')}") 
#     print(f"Is board full? {is_full(game_board)}")