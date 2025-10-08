ROWS = 6
COLUMNS = 7
EMPTY = "-" 

#saving and reading winners and their moves (Leaderboard Module)
def moves_file(moves_list):
   
    original_moves = {}

    try:
        
        with open("moves.txt", "r") as data:
            for line in data:
                line = line.strip()
                if ':' in line:
                    # name, move is like key and value in dict
                    name, move = line.split(":", 1) 
                    original_moves[name.strip()] = float(move.strip())
    except FileNotFoundError:
        pass  

   
    for player, new_move in moves_list.items():
        if player not in original_moves or new_move < original_moves[player]:
            original_moves[player] = new_move

          
    sorted_moves = dict(sorted(original_moves.items(), key=lambda x: x[1]))

  
    with open("moves.txt", "w") as file:
        for name, move in sorted_moves.items():
            # Ensure move is formatted cleanly for the file
            file.write(f"{name}: {move}\n")

   
    print("\n🏆 Leaderboard (Least Moves to Win):")
    print("____________________________________\n")
    rank = 1
    for name, move in sorted_moves.items():
        # Display the rank, name, and best move count
        print(f"{rank}. {name} - {move} moves")
        rank += 1


# Example of how to call the function:
if __name__ == "__main__":
    print("--- Example Usage ---")
    # This dictionary would typically come from the end of a Connect 4 game
    example_moves_list = {"Alice": 5.0, "Bob": 4.5} 
    
    # This function will update 'moves.txt' and print the leaderboard
    moves_file(example_moves_list)

   