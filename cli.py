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

p1_salt = "1234u128" # TODO: fix if more time
p2_salt = "1234u128" # TODO: fix if more time


def load_json(player):
    with open('program.json', 'w') as outfile:
        if player == "p1":
            json.dump(p1_program_json, outfile)
        else:
            json.dump(p2_program_json, outfile)

def print_board(board):
    int_board = int(board[:-4])
    for i in range(36):
        if i % 6 == 0 and i != 0:
            print(']\n', end="")
        if i % 6 == 0:
            print('[',end="")

        cur = (int_board & (2**(3*i)+2**(3*i +1)+2**(3*i +2))) >> (3*i)
        print(cur,end="")

        if i % 6 != 5:
            print(', ', end="")
    print("]\n")

pattern = r'\d+field'


# 1. init p1:
load_json("p1") # Set keys
p1_input_board = input("please input board in u128 encoding:") # Ask for board from user
print_board(p1_input_board)# 	# print board
os.system('leo ' + 'run ' + 'commit_board ' + p1_input_board + " " + p1_salt + ' false' ' > p1_hash.txt') # verify board
with open('p1_hash.txt', 'r') as file:
    content = file.read()
p1_commit_hash = re.search(pattern, content)
print("Hash commit of p2: " + p1_commit_hash.group())

# 2. init p2:
load_json("p2") # Set keys
p2_input_board = input("please input board in u128 encoding:") # Ask for board from user
print_board(p2_input_board)# 	# print board
os.system('leo ' + 'run ' + 'commit_board ' + p2_input_board + " " + p2_salt + ' true' ' > p2_hash.txt') # verify board
with open('p2_hash.txt', 'r') as file:
    content = file.read()
p2_commit_hash = re.search(pattern, content)
print("Hash commit of p2: " + p2_commit_hash.group())

def check_win(board):
    int_board = int(board[:-4])
    for i in range(36):
        cur = (int_board & (2**(3*i)+2**(3*i +1)+2**(3*i +2))) >> (3*i)
        if cur == 1:
            return False
    return True

def get_board(board):
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


def update_board(old, x1, y1, x2, y2, s, winner):
    if winner:
        return old - (int(s))*(2**(3*(6*int(x1) + int(y1)))) + (int(s))*(2**(3*(6*int(x2) + int(y2))))
    else:
        return old - (int(s))*(2**(3*(6*int(x1) + int(y1))))

game_won = 0

# 3. moves
player = ["p1","p2"]
counter = 0
p2_cur_board = p2_input_board
p2_cur_hash = p2_commit_hash
 
p1_cur_board = p1_input_board
p1_cur_hash = p2_commit_hash

while game_won == 0:

    # switch to Pi
    load_json(player[counter % 2])
    counter += 1

    # Ask for move:
    move = input("Please input move in format \'x1 y1 x2 y2 \'")
    x1 = move[0]
    y1 = move[2]
    x2 = move[4]
    y2 = move[6]

    # Check for combat
    b1 = get_board(p2_cur_board)
    b2 = get_board(p1_cur_board)

    # Assume legal move

    # Case combat 
    if (player == "p1" and b2[x2][y2] != 0) or (player == "p2" and b1[x2][y2] != 0):

        # Player 1 reveal
        load_json(player["p1"])
        os.system("leo run reveal_piece " + p1_cur_board + " " + p1_salt + " " + p1_cur_hash + " " + x2 + " " + y2)

        # Player 2 reveal
        load_json(player["p2"])
        os.system("leo run reveal_piece " + p2_cur_board + " " + p2_salt + " " + p2_cur_hash + " " + x2 + " " + y2)

        # Resolve combat
        result = input("combat winner in format \'winning_player piece loser_piece\': ") # TODO: add checks if have time
        if result[0:2] == "p2":
            b1[x2][y2] = 0
            b2[x1][y1] = 0
            b2[x2][y2] = result[3]

            # p2 winner update state
            load_json(player["p2"]) # verify move 
            os.system("leo run update_state " + p2_cur_board + " " + p2_salt + " " + p2_cur_hash + " " + x1 + " " + y1 + " " + x2 + " " + y2 + ' false' +  ' > p2_hash.txt')
            with open('p2_hash.txt', 'r') as file:
                content = file.read()
            p2_cur_hash = re.search(pattern, content)
            p2_cur_board = update_board(p2_cur_board, x1,y1,x2,y2, result[3], True)

            # p1 loser update state
            load_json(player["p1"]) # verify move 
            os.system("leo run update_state " + p1_cur_board + " " + p1_salt + " " + p1_cur_hash + " " + x1 + " " + y1 + " " + x2 + " " + y2 + ' true' +  ' > p1_hash.txt')
            with open('p1_hash.txt', 'r') as file:
                content = file.read()
            p1_cur_hash = re.search(pattern, content)
            p1_cur_board = update_board(p1_cur_board, x1,y1,x2,y2,result[5], False)

        else: 
            b1[x2][y2] = result[3]
            b1[x1][y1] = 0
            b2[x2][y2] = 0

            # p2 loser update state
            load_json(player["p2"]) # verify move 
            os.system("leo run update_state " + p2_cur_board + " " + p2_salt + " " + p2_cur_hash + " " + x1 + " " + y1 + " " + x2 + " " + y2 + ' false' +  ' > p2_hash.txt')
            with open('p2_hash.txt', 'r') as file:
                content = file.read()
            p2_cur_hash = re.search(pattern, content)
            p2_cur_board = update_board(p2_cur_board, x1,y1,x2,y2, result[3], True)

            # p1 winner update state
            load_json(player["p1"]) # verify move 
            os.system("leo run update_state " + p1_cur_board + " " + p1_salt + " " + p1_cur_hash + " " + x1 + " " + y1 + " " + x2 + " " + y2 + ' true' +  ' > p1_hash.txt')
            with open('p1_hash.txt', 'r') as file:
                content = file.read()
            p1_cur_hash = re.search(pattern, content)
            p1_cur_board = update_board(p1_cur_board, x1,y1,x2,y2,result[5], False)
    else:
        




# 	1. Move:
# 		1. Switch to pi
# 		2. Ask for (x1,y1)->(x2,y2)
# 		3. Check for combat?
# 			1. pi does verify
# 			2. switch to pi*
# 			3. pi* does verify
# 		4. Move

# board = 

# p1_board
# p2_board 


# def u128_to_board():

# def print_board():





