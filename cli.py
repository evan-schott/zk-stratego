import os
import json
import re
from pick import pick

p1_pk =  "APrivateKey1zkp6QHHh11csVkMWnVMSpgcySMu7YnwZABJ4FjvWQuQVPiX"
p1_vk =  "AViewKey1gfDcPVCcLZE6wyVZUpxXxcviD7jDNQRbqEh5L4CzeSTd"
p1_addr = "aleo1qm997nxje8378czqzxnjft47jjxhdgq23c2jw4leqv6k0ys4ngzq3fp9qh"

p2_pk =  "APrivateKey1zkp7mWwcLLxTcA2CyoKHfSgxv7cUKxNkQhJcDisUwpJLi4h"
p2_vk =  "AViewKey1eLahbMecbSj5bYbmfgkHKdHCtgFLdThtBafMAsVxYVi1"
p2_addr =  "aleo19uznaptte0k4mmvtxhfet4e9cgc0skzwd4a2xefeeay03ga89v9s4rj8gn"

player_board_arr = []
opp_player_board_arr = []
player_board_str = ""
opp_player_board_str = ""
player_hash = ""
opp_player_hash = ""
player_salt = ""
opp_player_salt = ""
player = ""
opp_player =""
last_i = -1
last_j = -1

p1_program_json = {
    "program": "stratego.aleo",
    "version": "0.0.0",
    "description": "",
    "development": {
        "private_key": p1_pk,
        "view_key": p1_vk,
        "address": p1_addr
    },
    "license": "MIT"
}

p2_program_json = {
    "program": "stratego.aleo",
    "version": "0.0.0",
    "description": "",
    "development": {
        "private_key": p2_pk,
        "view_key": p2_vk,
        "address": p2_addr
    },
    "license": "MIT"
}

p1_salt = "0u128" # TODO: fix if more time
p2_salt = "0u128" # TODO: fix if more time


def load_json(player):
    with open('program.json', 'w') as outfile:
        if player == "p1":
            json.dump(p1_program_json, outfile)
        else:
            json.dump(p2_program_json, outfile)


'''
Should look like: 
|---|---|---|---|---|---| 
| 0 | 0 | 0 | 0 | 0 | 0 |
|---|---|---|---|---|---| 
| 0 | 0 | 0 | 0 | 0 | 0 |
|---|---|---|---|---|---| 
| 0 | 0 | 0 | 0 | 0 | 0 |
|---|---|---|---|---|---| 
| 0 | 0 | 0 | 0 | 0 | 0 |
|---|---|---|---|---|---| 
| 4 | 4 | 5 | 5 | 6 | 7 |
|---|---|---|---|---|---| 
| 1 | 2 | 2 | 2 | 3 | 4 |
|---|---|---|---|---|---|

'''

VERTICAL_BORDER = '│'
HORIZONTAL_BORDER = '─'
TOP_LEFT = '┌'
TOP_RIGHT = '┐'
BOTTOM_LEFT = '└'
BOTTOM_RIGHT = '┘'
LEFT_BORDER = '├'
RIGHT_BORDER = '┤'
BOTTOM_BORDER = '┴'
TOP_BORDER = '┬'
CENTER = '┼'

TOP_LINE = TOP_LEFT + 3*HORIZONTAL_BORDER + TOP_BORDER + 3*HORIZONTAL_BORDER + TOP_BORDER + 3*HORIZONTAL_BORDER + TOP_BORDER + 3*HORIZONTAL_BORDER + TOP_BORDER + 3*HORIZONTAL_BORDER + TOP_BORDER + 3*HORIZONTAL_BORDER + TOP_RIGHT
MIDDLE_LINE = LEFT_BORDER + 3*HORIZONTAL_BORDER + CENTER + 3*HORIZONTAL_BORDER + CENTER + 3*HORIZONTAL_BORDER + CENTER + 3*HORIZONTAL_BORDER + CENTER + 3*HORIZONTAL_BORDER + CENTER + 3*HORIZONTAL_BORDER + RIGHT_BORDER
BOTTOM_LINE = BOTTOM_LEFT + 3*HORIZONTAL_BORDER + BOTTOM_BORDER + 3*HORIZONTAL_BORDER + BOTTOM_BORDER + 3*HORIZONTAL_BORDER + BOTTOM_BORDER + 3*HORIZONTAL_BORDER + BOTTOM_BORDER + 3*HORIZONTAL_BORDER + BOTTOM_BORDER + 3*HORIZONTAL_BORDER + BOTTOM_RIGHT

def print_red(text):
    red = "\033[31m"
    reset = "\033[0m"
    print(f"{red}{text}{reset}",end='')

def print_blue(text):
    blue = "\033[34m"
    reset = "\033[0m"
    print(f"{blue}{text}{reset}",end="")

    
def print_board_str(board):
    int_board = int(board[:-4]) # remove the 
    print("\n" + TOP_LINE)
    for i in range(36):
        if i % 6 == 0 and i != 0:
            print(VERTICAL_BORDER)
            print(MIDDLE_LINE)

        cur = (int_board & (2**(3*i)+2**(3*i +1)+2**(3*i +2))) >> (3*i)
        if cur == 0:
            print(VERTICAL_BORDER + ' ' + " " + ' ',end="")
        else:
            print(VERTICAL_BORDER + ' ' + str(cur) + ' ',end="")
    print(VERTICAL_BORDER)
    print(BOTTOM_LINE +"\n")

pattern = r'\d+field'


def parse_board(input_file):
    sum = 0
    exp = 1
    with open(input_file, 'r+') as f:
        grid = json.load(f)
        for row in grid:
            for num in row:
                sum += num * exp
                exp *= 8

        return str(sum) + "u128"

# 1. init p1:
load_json("p1") # Set keys
# p1_board = input("please input board in u128 encoding:") # Ask for board from user
p1_board_file = input("please provide the path to the file containing your board data:\n")
p1_board = parse_board(p1_board_file)
print("P1 private board state")
print_board_str(p1_board) 
os.system('leo ' + 'run ' + 'commit_board ' + p1_board + " " + p1_salt + ' false' + ' | tee -a ledger.txt > ' + 'p1_hash.txt') # verify board
with open('p1_hash.txt', 'r') as file:
    content = file.read()
p1_hash = re.search(pattern, content)
p1_hash = p1_hash.group()
print("P1 board verified.")
print("Hash commit=" + p1_hash)

# 2. init p2:
load_json("p2") # Set keys
p2_board_file = input("\n\nplease provide the path to the file containing your board data:\n") # Ask for board from user
p2_board = parse_board(p2_board_file)
print("P2 private board state")
print_board_str(p2_board)
os.system('leo ' + 'run ' + 'commit_board ' + p2_board + " " + p2_salt + ' true' + ' | tee -a ledger.txt > ' + 'p2_hash.txt') # verify board
with open('p2_hash.txt', 'r') as file:
    content = file.read()
p2_hash = re.search(pattern, content)
p2_hash = p2_hash.group()
print("P2 board verified.")
print("Hash commit=" + p2_hash)

# Scans board to see if own flag still stands
def check_if_i_lost(board):
    int_board = int(board[:-4])
    for i in range(36):
        cur = (int_board & (2**(3*i)+2**(3*i +1)+2**(3*i +2))) >> (3*i)
        if cur == 1:
            return False
    return True

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
def update_board_lose(board, i1, j1, val):
    int_board = int(board[:-4])
    return str(int_board - (int(val))*(2**(3*(6*int(i1) + int(j1))))) + "u128"

def pov_print_board_arr(hero_board, villain_board):
    arr = [
    [" ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " "]]
    for i in range(6):
        for j in range(6):
            if hero_board[i][j] != 0:
                arr[i][j] = hero_board[i][j]
            elif villain_board[i][j] != 0:
                arr[i][j] = "X"
    print_arr_board(arr)

def print_arr_board(board):
    print("\n" + TOP_LINE)
    for i in range(36):
        if i % 6 == 0 and i != 0:
            print(VERTICAL_BORDER)
            print(MIDDLE_LINE)
        if player == "p1":
            if str(board[int(i/6)][i%6]) in ["1","2","3","4","5","6","7"]:
                print(VERTICAL_BORDER + ' ',end="")
                print_blue(str(board[int(i/6)][i%6]))
                print(' ',end="")
            elif str(board[int(i/6)][i%6]) == "X":
                print(VERTICAL_BORDER + ' ',end="")
                print_red(str(board[int(i/6)][i%6]))
                print(' ',end="")
            else:
                print(VERTICAL_BORDER + ' ' + str(board[int(i/6)][i%6]) + ' ',end="")
        else:
            if str(board[int(i/6)][i%6]) in ["1","2","3","4","5","6","7"]:
                print(VERTICAL_BORDER + ' ',end="")
                print_red(str(board[int(i/6)][i%6]))
                print(' ',end="")
            elif str(board[int(i/6)][i%6]) == "X":
                print(VERTICAL_BORDER + ' ',end="")
                print_blue(str(board[int(i/6)][i%6]))
                print(' ',end="")
            else:
                print(VERTICAL_BORDER + ' ' + str(board[int(i/6)][i%6]) + ' ',end="")
        
    print(VERTICAL_BORDER)
    print(BOTTOM_LINE + "\n")

    return

def arr_board_to_str_board(board):
    int_board = 0
    for i in range(6):
        for j in range(6):
            int_board += (int(board[i][j]))*(2**(3*(6*int(i) + int(j))))

    return str(int_board) + "u128"


# Part 3: Players take turns moving
game_won = 0
players = ["p1","p2"]
counter = 0
while game_won == 0:
    # switch to Pi
    player = players[counter % 2]
    opp_player = players[(counter+1) % 2]
    counter += 1
    print(player + " is starting turn now!\n")

    # Check for combat
    # TODO: make sure that we update boards at end too

    if player == "p1":
        player_board_arr = str_board_to_arr_board(p1_board)
        opp_player_board_arr = str_board_to_arr_board(p2_board)
        player_board_str = p1_board
        opp_player_board_str = p2_board
        player_hash = p1_hash
        opp_player_hash = p2_hash
        player_salt = p1_salt
        opp_player_salt = p2_salt
    else:
        player_board_arr = str_board_to_arr_board(p2_board)
        opp_player_board_arr = str_board_to_arr_board(p1_board)
        player_board_str = p2_board
        opp_player_board_str = p1_board
        player_hash = p2_hash
        opp_player_hash = p1_hash
        player_salt = p2_salt
        opp_player_salt = p1_salt

    # Print updated board
    pov_print_board_arr(player_board_arr, opp_player_board_arr)

    # Ask for move: (Assume legal move)
    print("Please indicate which piece to move:")
    i1 = int(input("row: "))
    j1 = int(input("column: "))
    i2 = int(input("new row: "))
    j2 = int(input("new column: "))

    last_i = i2
    last_i = j2


    # Update State Functions
    # Case 1: Player killed
    def player_killed():
        global player
        global player_board_str
        global player_salt
        global player_hash

        load_json(player)
        os.system("leo run update_state " + player_board_str + " " + player_salt + " " + player_hash + " " + str(i1)+"u8" + " " + str(j1)+"u8" + " " + str(i2)+"u8" + " " + str(j2)+"u8" + ' true' + ' | tee -a ledger.txt > ' + player + '_hash.txt')
        with open(player + '_hash.txt', 'r') as file:
            content = file.read()
        player_hash = re.search(pattern, content)
        player_hash = player_hash.group()
        print("Player board verified.")
        print("New hash commit=" + player_hash) 

    # Case 2: Player moves
    def player_moves():

        global player
        global player_board_str
        global player_salt
        global player_hash
        load_json(player)
        os.system("leo run update_state " + player_board_str + " " + player_salt + " " + player_hash + " " + str(i1)+"u8" + " " + str(j1)+"u8" + " " + str(i2)+"u8" + " " + str(j2)+"u8" + ' false' + ' | tee -a ledger.txt > ' + player + '_hash.txt')
        with open(player + '_hash.txt', 'r') as file:
            content = file.read()
        player_hash = re.search(pattern, content)
        player_hash = player_hash.group()
        print("Player board verified.")
        print("New hash commit=" + player_hash)
    
    # Case: Opp killed
    def opp_killed():
        global opp_player
        global opp_player_board_str
        global opp_player_salt
        global opp_player_hash
        load_json(opp_player)
        os.system("leo run update_state " + opp_player_board_str + " " + opp_player_salt + " " + opp_player_hash + " " + str(i2)+"u8" + " " + str(j2)+"u8" + " " + str(i2)+"u8" + " " + str(j2)+"u8" + ' true' +  ' | tee -a ledger.txt > ' + opp_player + '_hash.txt')
        with open(opp_player + '_hash.txt', 'r') as file:
            content = file.read()
        opp_player_hash = re.search(pattern, content)
        opp_player_hash = opp_player_hash.group()
        print("Opponent player board verified.")
        print("New hash commit=" + opp_player_hash)

    # Case capture private key
    if opp_player_board_arr[i2][j2] == 1:
        print(player + " wins!!!\n\nGame over!!\n\n")
        exit(0)

    # Case combat 
    elif opp_player_board_arr[i2][j2] != 0:
        print("Verifying " + player + " proof of strength at (" + str(i1)+"u8" + "," + str(j1)+"u8" + ")")
        load_json(player)
        os.system("leo run reveal_piece " + player_board_str + " " + player_salt + " " + player_hash + " " + str(i1)+"u8" + " " + str(j1)+"u8" + " >> ledger.txt")

        print("Verifying " + opp_player + " proof of strength at (" + str(i2)+"u8" + "," + str(j2)+"u8" + ")")
        load_json(opp_player)
        os.system("leo run reveal_piece " + opp_player_board_str + " " + opp_player_salt + " " + opp_player_hash + " " + str(i2)+"u8" + " " + str(j2)+"u8"+ " >> ledger.txt")

        # Case: Miner attacks hash puzzle
        if opp_player_board_arr[i2][j2] == 2 and player_board_arr[i1][j1] == 5:
            opp_killed()
            player_moves()

            player_board_str = update_board_win(player_board_str,i1,j1,i2,j2,5)
            opp_player_board_str = update_board_lose(opp_player_board_str,i2,j2,2)


        # Case: Anyone else attacks hashpuzzle
        elif opp_player_board_arr[i2][j2] == 2:
            player_killed()

            player_board_str = update_board_lose(player_board_str,i1,j1,player_board_arr[i1][j1])

        # Case: Whistleblower attacks CEO 
        elif opp_player_board_arr[i2][j2] == 7 and player_board_arr[i1][j1] == 3:
            opp_killed()
            player_moves()

            player_board_str = update_board_win(player_board_str,i1,j1,i2,j2,3)
            opp_player_board_str = update_board_lose(opp_player_board_str,i2,j2,7)

        # Case: CEO attacks Whistleblower 
        elif opp_player_board_arr[i2][j2] == 3 and player_board_arr[i1][j1] == 7:
            player_killed()
            player_board_str = update_board_lose(player_board_str,i1,j1,7)

        # Case: Lower strength => player dies
        elif opp_player_board_arr[i2][j2] > player_board_arr[i1][j1]:
            player_killed()
            player_board_str = update_board_lose(player_board_str,i1,j1,player_board_arr[i1][j1])

        # Case: Equal strength => both die
        elif opp_player_board_arr[i2][j2] == player_board_arr[i1][j1]:
            opp_killed()
            player_killed()
            player_board_str = update_board_lose(player_board_str,i1,j1,player_board_arr[i1][j1])
            opp_player_board_str = update_board_lose(opp_player_board_str,i2,j2, opp_player_board_arr[i2][j2])

        # Case: Greater strength => opp dies
        elif opp_player_board_arr[i2][j2] < player_board_arr[i1][j1]:
            opp_killed()
            player_moves()
            opp_player_board_str = update_board_lose(opp_player_board_str,i2,j2, opp_player_board_arr[i2][j2])
            player_board_str = update_board_win(player_board_str,i1,j1,i2,j2,player_board_arr[i1][j1])

    # Case: Normal movement
    else: 
        player_moves()
        player_board_str = update_board_win(player_board_str,i1,j1,i2,j2,player_board_arr[i1][j1])

    # Update player and opp player info (board, hash)
    if player == "p1":
        p1_board = player_board_str
        p2_board = opp_player_board_str
        p1_hash = player_hash
        p2_hash = opp_player_hash
    else:
        p2_board = player_board_str
        p1_board = opp_player_board_str
        p2_hash = player_hash
        p1_hash = opp_player_hash
