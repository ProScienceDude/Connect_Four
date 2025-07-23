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

#saving and reading winners and their moves
def moves_file(moves_list):
    original_moves = {}

    try:
        with open("moves.txt", "r") as data:
            for line in data:
                if ':' in line:
                    name, move = line.split(":") #name, move is like key and value in cict voh specify karne ki zarutat nai
                    original_moves[name] = float(move)
    except FileNotFoundError:
        pass  # first time file ddoes not exist

    # Updating if moves is better
    for player, new_move in moves_list.items():
        if player not in original_moves or new_move < original_moves[player]:
            original_moves[player] = new_move

    #Arranging players according to no of moves        
    sorted_moves = dict(sorted(original_moves.items(), key=lambda x: x[1]))

    with open("moves.txt", "w") as file:
        for name, move in sorted_moves.items():
            file.write(f"{name}: {move}\n")

    # Print leaderboard
    print("\n🏆 Leaderboard (Least Moves to Win):")
    print("____________________________________\n")
    rank = 1
    for name, move in sorted_moves.items():
        print(f"{rank}. {name} - {move} moves")
        rank += 1


#Main game loop
def play_game():
    board = create_board()
    turn = 0
    game_over = False

    print("Welcome to Connect 4!")

    # Ask player names
    players = {
        "X": input("Enter name for Player X: "),
        "O": input("Enter name for Player O: ")
    }


    print_board(board)

    while not game_over:
        piece = "X" if turn % 2 == 0 else "O"
        player = players[piece]

        try:
            column = int(input(f"{player} ({piece}), choose a column (0-{COLUMNS-1}): "))
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
            winner = player
            if turn % 2 == 0:
                move = (turn + 2) / 2
            else:
                move = (turn + 1) / 2  
            print(f"\n {player} ({piece}) wins with a total of {move} moves")  
            game_over = True
        elif is_full(board):
            print("It's a draw!")
            game_over = True
        else:
            turn += 1


    moves_list = {winner : move , }
    print("\n" , "Winners and moves required to win", "\n")
    moves_file(moves_list)
       
#Calling game
if __name__ == "__main__":
    play_game()
