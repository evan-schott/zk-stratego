import os
import json
import re

p1_pk =  "APrivateKey1zkp6QHHh11csVkMWnVMSpgcySMu7YnwZABJ4FjvWQuQVPiX"
p1_vk =  "AViewKey1gfDcPVCcLZE6wyVZUpxXxcviD7jDNQRbqEh5L4CzeSTd"
p1_addr = "aleo1qm997nxje8378czqzxnjft47jjxhdgq23c2jw4leqv6k0ys4ngzq3fp9qh"

p2_pk =  "APrivateKey1zkp7mWwcLLxTcA2CyoKHfSgxv7cUKxNkQhJcDisUwpJLi4h"
p2_vk =  "AViewKey1eLahbMecbSj5bYbmfgkHKdHCtgFLdThtBafMAsVxYVi1"
p2_addr =  "aleo19uznaptte0k4mmvtxhfet4e9cgc0skzwd4a2xefeeay03ga89v9s4rj8gn"

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

pattern = r'\d+field'


# 1. init p1:
load_json("p1") # Set keys
p1_board = input("please input board in u128 encoding:") # Ask for board from user
print("P1 private board state")
print_board_str(p1_board)
os.system('leo ' + 'run ' + 'commit_board ' + p1_board + " " + p1_salt + ' false' ' > p1_hash.txt') # verify board
with open('p1_hash.txt', 'r') as file:
    content = file.read()
p1_commit_hash = re.search(pattern, content)
p1_commit_hash = p1_commit_hash.group()
print("P1 board verified.")
print("Hash commit=" + p1_commit_hash)

# 2. init p2:
load_json("p2") # Set keys
p2_board = input("\n\nplease input board in u128 encoding:") # Ask for board from user
print("P2 private board state")
print_board_str(p2_board)
os.system('leo ' + 'run ' + 'commit_board ' + p2_board + " " + p2_salt + ' true' ' > p2_hash.txt') # verify board
with open('p2_hash.txt', 'r') as file:
    content = file.read()
p2_commit_hash = re.search(pattern, content)
p2_commit_hash = p2_commit_hash.group()
print("P2 board verified.")
print("Hash commit=" + p2_commit_hash)


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
    player_board_arr = []
    opp_player_board_arr = []
    player_board_str = ""
    opp_player_board_str = ""
    player_hash = ""
    opp_player_hash = ""
    player_salt = ""
    opp_player_salt = ""

    if player == "p1":
        player_board_arr = str_board_to_arr_board(p1_board)
        opp_player_board_arr = str_board_to_arr_board(p2_board)
        player_board_str = p1_board
        opp_player_board_str = p2_board
        player_hash = p1_commit_hash
        opp_player_hash = p2_commit_hash
        player_salt = p1_salt
        opp_player_salt = p2_salt
    else:
        player_board_arr = str_board_to_arr_board(p2_board)
        opp_player_board_arr = str_board_to_arr_board(p1_board)
        player_board_str = p2_board
        opp_player_board_str = p1_board
        player_hash = p2_commit_hash
        opp_player_hash = p1_commit_hash
        player_salt = p2_salt
        opp_player_salt = p1_salt

    # Ask for move: (Assume legal move)
    move = input("Please input move in format \'i1 j1 i2 j2 \'")
    i1 = int(move[0])
    j1 = int(move[2])
    i2 = int(move[4])
    j2 = int(move[6])

    # Case combat 
    if opp_player_board_arr[i2][j2] == 1:
        print(player + " wins!!!\n\nGame over!!\n\n")
        exit(0)

    elif opp_player_board_arr[i2][j2] != 0:
        print("Verifying " + player + " proof of strength at (" + str(i1) + "," + str(j1) + ")")
        load_json(player)
        os.system("leo run reveal_piece " + player_board_str + " " + player_salt + " " + player_hash + " " + str(i1) + " " + str(j1))

        print("Verifying " + opp_player + " proof of strength at (" + str(i2) + "," + str(j2) + ")")
        load_json(opp_player)
        os.system("leo run reveal_piece " + opp_player_board_str + " " + opp_player_salt + " " + opp_player_hash + " " + str(i2) + " " + str(j2))

        # Case: Miner attacks hash puzzle
        if opp_player_board_arr[i2][j2] == 2 and player_board_arr[i1][j1] == 5:
            player_board_str = update_board_win(player_board_str,i1,j1,i2,j2,5)
            opp_player_board_str = update_board_lose(opp_player_board_str,i2,j2,2)

        # Case: Anyone else attacks hashpuzzle
        elif opp_player_board_arr[i2][j2] == 2:
            player_board_str = update_board_lose(player_board_str,i1,j1,player_board_arr[i1][j1])

        # Case: Whistleblower attacks CEO 
        elif opp_player_board_arr[i2][j2] == 7 and player_board_arr[i1][j1] == 3:
            player_board_str = update_board_win(player_board_str,i1,j1,i2,j2,3)
            opp_player_board_str = update_board_lose(opp_player_board_str,i2,j2,7)

        # Case: CEO attacks Whistleblower 
        elif opp_player_board_arr[i2][j2] == 3 and player_board_arr[i1][j1] == 7:
            player_board_str = update_board_lose(player_board_str,i1,j1,7)

        # Case: Lower strength
        elif opp_player_board_arr[i2][j2] > player_board_arr[i1][j1]:
            player_board_str = update_board_lose(player_board_str,i1,j1,player_board_arr[i1][j1])

        # Case: Equal strength
        elif opp_player_board_arr[i2][j2] == player_board_arr[i1][j1]:
            player_board_str = update_board_lose(player_board_str,i1,j1,player_board_arr[i1][j1])

        # Case: Greater strength
        elif opp_player_board_arr[i2][j2] == player_board_arr[i1][j1]:




    # This is mess
    if (player == "p1" and b2[int(x2)][int(y2)] != 0) or (player == "p2" and b1[int(x2)][int(y2)] != 0):

        # Player 1 reveal
        load_json("p1")
        os.system("leo run reveal_piece " + p1_cur_board + " " + p1_salt + " " + p1_cur_hash + " " + x2 + " " + y2)

        # Player 2 reveal
        load_json("p2")
        os.system("leo run reveal_piece " + p2_cur_board + " " + p2_salt + " " + p2_cur_hash + " " + x2 + " " + y2)

        # Resolve combat
        result = input("combat winner in format \'winning_player piece loser_piece\': ") # TODO: add checks if have time
        if result[0:2] == "p2":
            b1[int(x2)][int(y2)] = 0
            b2[int(x1)][int(y1)] = 0
            b2[int(x2)][int(y2)] = result[3]

            # p2 winner update state
            load_json("p2") # verify move 
            os.system("leo run update_state " + p2_cur_board + " " + p2_salt + " " + p2_cur_hash + " " + x1 + " " + y1 + " " + x2 + " " + y2 + ' false' +  ' > p2_hash.txt')
            with open('p2_hash.txt', 'r') as file:
                content = file.read()
            p2_cur_hash = re.search(pattern, content)
            p2_cur_board = update_board(p2_cur_board, int(x1), int(y1), int(x2), int(y2), int(result[3]), True)
            p2_cur_board = get_board(p2_cur_board)

            # p1 loser update state
            load_json("p1") # verify move 
            os.system("leo run update_state " + p1_cur_board + " " + p1_salt + " " + p1_cur_hash + " " + x1 + " " + y1 + " " + x2 + " " + y2 + ' true' +  ' > p1_hash.txt')
            with open('p1_hash.txt', 'r') as file:
                content = file.read()
            p1_cur_hash = re.search(pattern, content)
            p1_cur_board = update_board(p1_cur_board, int(x1), int(y1), int(x2), int(y2), int(result[5]), False)
            p1_cur_board = get_board(p1_cur_board)

        else: 
            b1[int(x2)][int(y2)] = result[3]
            b1[int(x1)][int(y1)] = 0
            b2[int(x2)][int(y2)] = 0

            # p2 loser update state
            load_json("p2") # verify move 
            os.system("leo run update_state " + p2_cur_board + " " + p2_salt + " " + p2_cur_hash + " " + x1 + " " + y1 + " " + x2 + " " + y2 + ' true' +  ' > p2_hash.txt')
            with open('p2_hash.txt', 'r') as file:
                content = file.read()
            p2_cur_hash = re.search(pattern, content)
            p2_cur_board = update_board(p2_cur_board, int(x1), int(y1), int(x2), int(y2), int(result[5]), False)
            p2_cur_board = get_board(p2_cur_board)

            # p1 winner update state
            load_json("p1") # verify move 
            os.system("leo run update_state " + p1_cur_board + " " + p1_salt + " " + p1_cur_hash + " " + x1 + " " + y1 + " " + x2 + " " + y2 + ' false' +  ' > p1_hash.txt')
            with open('p1_hash.txt', 'r') as file:
                content = file.read()
            p1_cur_hash = re.search(pattern, content)
            p1_cur_board = update_board(p1_cur_board, int(x1), int(y1), int(x2), int(y2), int(result[3]), True)
            p1_cur_board = get_board(p1_cur_board)
    
    # normal move
    else:
        if player == "p2":
            os.system("leo run update_state " + player + " " + p2_salt + " " + p2_cur_hash + " " + x1 + " " + y1 + " " + x2 + " " + y2 + ' false' +  ' > p2_hash.txt')
            with open('p2_hash.txt', 'r') as file:
                content = file.read()
            p2_cur_hash = re.search(pattern, content)
            
        else:
            os.system("leo run update_state " + player + " " + p1_salt + " " + p1_cur_hash + " " + x1 + " " + y1 + " " + x2 + " " + y2 + ' false' +  ' > p1_hash.txt')
            with open('p1_hash.txt', 'r') as file:
                content = file.read()
            p1_cur_hash = re.search(pattern, content)
    
    print("P1 Board:")
    print_board(p1_cur_board)
    print("P2 Board:")
    print_board(p2_cur_board)


    p2_win = check_win(p1_cur_board)
    p1_win = check_win(p2_cur_board)

    if p1_win:
        print("P1 WIN")
        game_won = 1
    if p2_win:
        print("P2 WIN")
        game_won = 2
    

