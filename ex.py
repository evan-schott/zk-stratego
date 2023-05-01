def print_board_str(board):
    int_board = int(board[:-4]) # remove the 
    print("\n|---|---|---|---|---|---|")
    for i in range(36):
        if i % 6 == 0 and i != 0:
            print('|')
            print('|---|---|---|---|---|---|')

        cur = (int_board & (2**(3*i)+2**(3*i +1)+2**(3*i +2))) >> (3*i)
        print('| ' + str(cur) + ' ',end="")
    print("|")
    print("|---|---|---|---|---|---|\n")

# Converts to array representation
def str_board_to_arr_board(board):
    arr = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]]
    int_board = int(board[:-4])
    for i in range(36):
        arr[int(i/6)][i%6] = (int_board & (2**(3*i)+2**(3*i +1)+2**(3*i +2))) >> (3*i)
    return arr

# Move your piece
def update_board_win(board, i1, j1, i2, j2, val):
    int_board = int(board[:-4])
    return str(int_board - (int(val))*(2**(3*(6*int(i1) + int(j1)))) + (int(val))*(2**(3*(6*int(i2) + int(j2)))))+"u128"

# Remove your piece from board
def update_board_lose(board, i1, j1, i2, j2, val):
    int_board = int(board[:-4])
    return str(int_board - (int(val))*(2**(3*(6*int(i1) + int(j1)))) + (int(val))*(2**(3*(6*int(i2) + int(j2)))))+"u128"


def pov_print_board_arr(hero_board, villain_board):
    arr = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]]
    for i in range(6):
        for j in range(6):
            if hero_board[i][j] != 0:
                arr[i][j] = hero_board[i][j]
            elif villain_board[i][j] != 0:
                arr[i][j] = "X"
    print_arr_board(arr)

def print_arr_board(board):
    print("\n|---|---|---|---|---|---|")
    for i in range(36):
        if i % 6 == 0 and i != 0:
            print('|')
            print('|---|---|---|---|---|---|')
        print('| ' + str(board[int(i/6)][i%6]) + ' ',end="")
    print("|")
    print("|---|---|---|---|---|---|\n")

    return

def arr_board_to_str_board(board):
    int_board = 0
    for i in range(6):
        for j in range(6):
            int_board += (int(board[i][j]))*(2**(3*(6*int(i) + int(j))))

    return str(int_board) + "u128"


# print(str_board_to_arr_board("67472864401u128"))
p1_board = "67472864401u128"
p2_board = "318631593350490860862688876036096u128"
print_board_str(p1_board)
print_board_str(p2_board)
pov_print_board_arr(str_board_to_arr_board(p1_board),str_board_to_arr_board(p2_board))
p1_board = update_board_win(p1_board,1,0,2,0,4)
pov_print_board_arr(str_board_to_arr_board(p1_board),str_board_to_arr_board(p2_board))
p1_board_arr = str_board_to_arr_board(p1_board)
p1_board_arr[0][0]=0
pov_print_board_arr(p1_board_arr,str_board_to_arr_board(p2_board))

# p1_board = update_board_win(p1_board,1,0,2,0,4)
# print_board_str(p1_board)
# p1_board = update_board_win(p1_board,2,0,3,0,4)
# print_board_str(p1_board)



# print_board_str("67472864401u128")
# print_board_str("318631593350490860862688876036096u128")
# print(check_win("67472864401u128"))
# print(check_win("24u128"))