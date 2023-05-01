import json

json_data=open('./player1board.json')

sum = 0
exp = 1
with open('player1board.json', 'r+') as f:
    grid = json.load(f)
    for row in grid:
        for num in row:
            sum += num * exp
            exp *= 8

    print(sum)