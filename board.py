import matplotlib.pyplot as plt
import matplotlib.patches as patches
from connect4 import create_board, drop_piece_at, get_available_row, check_win, is_full

ROWS, COLUMNS = 6, 7
board = create_board()
turn = 0
game_over = False

fig, ax = plt.subplots()
plt.axis('off')

def draw_board():
    ax.clear()
    ax.set_xlim(0, COLUMNS)
    ax.set_ylim(0, ROWS)
    ax.set_aspect('equal')
    plt.axis('off')

    # Draw grid
    for r in range(ROWS):
        for c in range(COLUMNS):
            ax.add_patch(patches.Rectangle((c, r), 1, 1, edgecolor='black', facecolor='blue'))
            piece = board[ROWS - 1 - r][c]  # invert for correct visual
            if piece in ("X", "O"):
                ax.text(c + 0.5, r + 0.5, piece, ha='center', va='center', fontsize=20, color='white')

    plt.draw()

def on_click(event):
    global turn, game_over

    if game_over or event.xdata is None:
        return

    col = int(event.xdata)
    row = get_available_row(board, col)

    if row is not None:
        piece = "X" if turn % 2 == 0 else "O"
        drop_piece_at(board, row, col, piece)
        draw_board()

        if check_win(board, piece):
            ax.set_title(f"Player {piece} wins!", fontsize=16)
            game_over = True
        elif is_full(board):
            ax.set_title("It's a draw!", fontsize=16)
            game_over = True
        else:
            turn += 1

    plt.draw()

fig.canvas.mpl_connect("button_press_event", on_click)
draw_board()
plt.show()
