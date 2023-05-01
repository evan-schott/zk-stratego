import os
import json
import re
from pick import pick
import json
import time

record = "\'{owner: aleo1rhgdu77hgyqd3xjj8ucu3jj9r2krwz6mnzyd80gncr5fxcwlh5rsvzp9px.private, microcredits: 375000000000000u64.private, _nonce: 7878975746507090126227171979105950023927846325862272020500118522178700349837group.public}\'"



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


# title = 'Please choose your favorite programming language (press SPACE to mark, ENTER to continue): '
# options = ['Java', 'JavaScript', 'Python', 'PHP', 'C++', 'Erlang', 'Haskell']
# selected = pick(options, title, min_selection_count=1)
# print(selected)

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
# os.system('leo ' + 'run ' + 'commit_board ' + p1_board + " " + p1_salt + ' false' + ' | tee -a ledger.txt > ' + 'p1_hash.txt') # verify board
print('snarkos developer execute stratego.aleo' + ' commit_board' + ' \"' + p1_board + '\" ' + ' \"' + p1_salt + '\" ' + '\"false\"' + ' --private-key APrivateKey1zkp8CZNn3yeCseEtxuVPbDCwSyhGW6yZKUYKfgXmcpoGPWH --query "http://localhost:3030" --broadcast "http://localhost:3030/testnet3/transaction/broadcast" --fee 60000000 --record ' + record + ' | tee -a ledger.txt > ' + 'output.txt')
os.system('snarkos developer execute stratego.aleo' + ' commit_board' + ' \"' + p1_board + '\" ' + ' \"' + p1_salt + '\" ' + '\"false\"' + ' --private-key APrivateKey1zkp8CZNn3yeCseEtxuVPbDCwSyhGW6yZKUYKfgXmcpoGPWH --query "http://localhost:3030" --broadcast "http://localhost:3030/testnet3/transaction/broadcast" --fee 60000000 --record ' + record + ' | tee -a ledger.txt > ' + 'output.txt')
tx_id_regex_pattern = r'(?<=\n)at[^\n]*(?=\n)'
with open('output.txt', 'r') as file:
    content = file.read()
tx_id = re.search(tx_id_regex_pattern, content)
tx_id = tx_id.group()
print(tx_id)

print('curl -X GET http://localhost:3030/testnet3/transaction/' + tx_id + ' > intermediate.json')

time.sleep(1)
os.system('curl -X GET http://localhost:3030/testnet3/transaction/' + tx_id)
time.sleep(1)
with open("intermediate.json", 'r') as file:
    data = json.load(file)
    record = data["fee"]["transition"]["outputs"][0]["value"]
os.system('snarkos developer decrypt --ciphertext ' + record + ' --view-key AViewKey1mSnpFFC8Mj4fXbK5YiWgZ3mjiV8CxA79bYNa8ymUpTrw > decrypted_record.txt')

with open("decrypted_record.txt", 'r') as file:
    record = file.read().replace("\n","")
p1_hash = data["execution"]["transitions"][0]["outputs"][0]["value"]
print(record)
print("P1 board verified.")
print("Hash commit=" + p1_hash)


