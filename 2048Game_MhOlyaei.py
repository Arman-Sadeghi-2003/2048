
from tkinter import *
import numpy as np

grid_cells = []

colorsDict = {2: "#daeddf", 4: "#9ae3ae", 
              8: "#6ce68d", 16: "#42ed71",
              32: "#17e650", 64: "#17c246", 
              128: "#149938", 256: "#107d2e", 
              512: "#0e6325", 1024: "#0b4a1c",
              2048: "#031f0a", 4096: "#000000", 
              8192: "#000000",}

colors = {2: "#011c08", 4: "#011c08", 
          8: "#011c08", 16: "#011c08",
          32: "#011c08", 64: "#f2f2f0", 
          128: "#f2f2f0", 256: "#f2f2f0", 
          512: "#f2f2f0", 1024: "#f2f2f0",
          2048: "#f2f2f0", 4096: "#f2f2f0", 
          8192: "#f2f2f0",}



def push_board_right(board):
    new = np.zeros((4, 4), dtype="int")
    done = False
    for row in range(4):
        count = 4 - 1
        for col in range(4 - 1, -1, -1):
            if board[row][col] != 0:
                new[row][count] = board[row][col]
                if col != count:
                    done = True
                count -= 1
    return (new, done)


def merge_elements(board):
    score = 0
    done = False
    for row in range(4):
        for col in range(4 - 1, 0, -1):
            if board[row][col] == board[row][col-1] and board[row][col] != 0:
                board[row][col] *= 2
                score += board[row][col]
                board[row][col-1] = 0
                done = True
    return (board, done, score)


def move_up(board):
    rotated_board = np.rot90(board, -1)
    pushed_board, has_pushed = push_board_right(rotated_board)
    merged_board, has_merged, score = merge_elements(pushed_board)
    second_pushed_board, _ = push_board_right(merged_board)
    rotated_back_board = np.rot90(second_pushed_board)
    move_made = has_pushed or has_merged
    return rotated_back_board, move_made, score

    
def move_down(board):
    board = np.rot90(board)
    board, has_pushed = push_board_right(board)
    board, has_merged, score = merge_elements(board)
    board, _ = push_board_right(board)
    board = np.rot90(board, -1)
    move_made = has_pushed or has_merged
    return board, move_made, score


def move_left(board):
    board = np.rot90(board, 2)
    board, has_pushed = push_board_right(board)
    board, has_merged, score = merge_elements(board)
    board, _ = push_board_right(board)
    board = np.rot90(board, -2)
    move_made = has_pushed or has_merged
    return board, move_made, score


def move_right(board):
    board, has_pushed = push_board_right(board)
    board, has_merged, score = merge_elements(board)
    board, _ = push_board_right(board)
    move_made = has_pushed or has_merged
    return board, move_made, score


def add_new_tile(board):
    tile_value = np.array([2, 2, 2, 2, 2, 2, 2, 2 ,2, 4])[np.random.randint(0, len(np.array([2, 2, 2, 2, 2, 2, 2, 2 ,2, 4])))]
    tile_row_options, tile_col_options = np.nonzero(np.logical_not(board))
    tile_loc = np.random.randint(0, len(tile_row_options))
    board[tile_row_options[tile_loc], tile_col_options[tile_loc]] = tile_value
    return board

                      

window = Tk()
window.grid()
window.title('2048 بازی - AILC')


matrix = np.zeros((16), dtype="int")
initial_twos = np.random.default_rng().choice(16, 2, replace=False)
matrix[initial_twos] = 2
matrix = matrix.reshape((4, 4))

def key_press( event):
    global matrix

    valid_game = True
    key = repr(event.char)
    commands = {"'w'": move_up, 
                "'s'": move_down,
                "'a'": move_left, 
                "'d'": move_right}
    
    if key in commands:
        matrix, move_made, _ = commands[repr(event.char)](matrix)
        if move_made:
            matrix = add_new_tile(matrix)
            for row in range(4):
                for col in range(4):
                    tile_value = matrix[row][col]
                    if not tile_value:
                        grid_cells[row][col].configure(
                            text="", bg="#8eaba8")
                    else:
                        grid_cells[row][col].configure(text=str(
                            tile_value), bg=colorsDict[tile_value],
                            fg=colors[tile_value])
            window.update_idletasks()
            move_made = False


window.bind("<Key>", key_press)

    
background = Frame(window, bg="#a6bdbb",
                   width=400, height=400)
background.grid()

for row in range(4):
    grid_row = []
    for col in range(4):
        cell = Frame(background, bg="#8eaba8",
                     width=400 / 4,
                     height=400 / 4)
        cell.grid(row=row, column=col, padx=10,
                  pady=10)
        t = Label(master=cell, text="",
                  bg="#8eaba8",
                  justify=CENTER, font=("B Nazanin", 20, "bold"), width=5, height=2)
        t.grid()
        grid_row.append(t)

    grid_cells.append(grid_row)
    


for row in range(4):
    for col in range(4):
        tile_value = matrix[row][col]
        if not tile_value:
            grid_cells[row][col].configure(
                text="", bg="#8eaba8")
        else:
            grid_cells[row][col].configure(text=str(
                tile_value), bg=colorsDict[tile_value],
                fg=colors[tile_value])
window.update_idletasks()
window.mainloop()