ROWS = 6
COLUMNS = 7
EMPTY = "-"

#Creating board
def create_board():
    return [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]

#Printing board
def print_board(board):
    for row in board:
        print(" ".join(row))
    print(" ".join([str(i) for i in range(COLUMNS)]))  # column numbers

#Dropping piece
def drop_piece(board, column, piece):
    for row in reversed(board):
        if row[column] == EMPTY:
            row[column] = piece
            return True
    return False  #Column bhar gya

#Checking win condition
def check_win(board, piece):
    #Horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    #Vertical
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    #Diagonal niche-right
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    #Diagonal upar-left
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False

#Checking if board if full
def is_full(board):
    return all(cell != EMPTY for row in board for cell in row)

#Main game loop
def play_game():
    board = create_board()
    turn = 0
    game_over = False

    print("Welcome to Connect 4!")
    print_board(board)

    while not game_over:
        piece = "X" if turn % 2 == 0 else "O"
        try:
            column = int(input(f"Player {piece}, choose a column (0-{COLUMNS-1}): "))
            if column < 0 or column >= COLUMNS:
                print("Invalid column. Try again.")
                continue
        except ValueError:
            print("Invalid input. Enter a number.")
            continue

        if not drop_piece(board, column, piece):
            print("Column full. Try a different one.")
            continue

        print_board(board)

        if check_win(board, piece):
            print(f"Player {piece} wins!")
            game_over = True
        elif is_full(board):
            print("It's a draw!")
            game_over = True
        else:
            turn += 1


def get_available_row(board, column):
    for r in range(ROWS - 1, -1, -1):
        if board[r][column] == EMPTY:
            return r
    return None  # Column full

def drop_piece_at(board, row, column, piece):
    board[row][column] = piece            

#Calling game
if __name__ == "__main__":
    play_game()
