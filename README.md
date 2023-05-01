![Mini Stratego Logo](./logo.png "Mini Stratego Logo")

This is an Aleo implementation of a slightly smaller version of Stratego. The board is 6x6.

## Gameplay
The original Stratego is military themed, but we chose to use a __✅ crypto company ✅__ theme for our mini implementation. Each side has the following pieces:

| Name        | Description      | Quantity  | Strength
| ------------- |:-------------:|:-----:| -----:|
| Flag      | goal is to capture it | 1 | N/A |
| Hash puzzle      | so tough that only a miner can solve (aka capture) it      | 3 | 10 |
| Whistleblower | no one likes them anymore :(      | 1 | 1 |
| Intern | might be a newcomer, but still more loved than the whistleblower      |   2 | 2 |
| Miner | can "defuse" the hash puzzles.      |   2 | 3 |
| Dev | beats everyone except the CEO.      |   2 | 4 |
| CEO | only the whistleblower can kill it :)      |  1 | 5 |

A corollary is that at the beginning, each player has 16 pieces on their board and 24 empty squares (the opponent's pieces are not noted).

The game flow:
1. Each player decides on a configuration for their pieces.
2. Players send each other commitments to their piece configuration (`commit_board`).
3. Player 1 makes a move and sends player 2 a proof that the move was valid and a commitment to their new position (`update_state`).
4. Player 2 makes a move and sends player 1 a proof that the move was valid and a commitment to their new position (`update_state`).
5. Repeat steps 3 and 4 until a player decides to attack. In case of an attack, both sides need to reveal the type of the piece that is attacking/being attacked (`reveal_piece`). The weaker piece gets killed (`update_state`), and if the attacker piece was the stronger piece, then it moves to the victim's position (`update_state`).
6. Repeat steps 3, 4, and 5 until a flag is captured.



## Functions
We took great care in minimizing the computations done by the zk circuits. Below are details about each function.
* `update_state`: When a player's piece configuration changes, the commitment to their old board is no longer relevant. So, they need to generate a new one. A piece configuration can change if 1) a piece simply gets moved, 2) a piece gets attacked by a stronger piece and killed, 3) a piece tries to attack a stronger piece but gets killed, 4) a piece attacks a weaker piece and replaced it on the board. This function proves that the board being updated is the board representing the last state of the piece configuration before the update. It then moves or removes the relevant piece on/from the board as necessary.
* `reveal_piece`: When a piece attacks/gets attacked by another piece, both players need to announce the types of their pieces. The strengths of the pieces then get compared. This function reveals the type of the piece in the given location while proving that it is using the most recent state of the board. Note that this function does not do any bound checks for the position: because the location is public, the prover must input meaningful positions. Otherwise, the opponent will not get convinced. If the location was private, we would have had to do bound checks.
* `commit_board`: Each player needs to assure their opponent that the way they place their piece on the board is valid. However, they are not supposed to reveal which piece is where. In other words, for every position on the board, the opponent should only know whether there is a piece there or not. They shouldn't learn the type of the piece. This function produces a hash that acts as a commitment to the piece configuration. When making the next move, this hash value is referenced to prove that no piece has been sneakily moved since the last public move.

## CLI
We have built a neat CLI for people to play with the circuits. After making sure that you have Python installed, run the following command to start the CLI:
```
python3 cli.py
```
The CLI asks both players to place their pieces on the board. To do this, player 1 can edit `player1board.py` while player 2 can edit `player2board.py`.

### Note on deployment
The current version is not deployed on the testnet, but we have made significant progress on deploying to the local node. Our efforts can be seen in `cli_deploy.py`. 

<details><summary>Sample game</summary>

```
$ python3 cli.py
please provide the path to the file containing your board data:
player1board.json
P1 private board state

┌───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 4 │ 5 │ 3 │ 4 │
├───┼───┼───┼───┼───┼───┤
│ 2 │ 2 │ 5 │ 6 │ 6 │ 7 │
├───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │   │
└───┴───┴───┴───┴───┴───┘

P1 board verified.
Hash commit=399577396980623581895515715827396235068708917853474010135638094251711625443field


please provide the path to the file containing your board data:
player2board.json            
P2 private board state

┌───┬───┬───┬───┬───┬───┐
│   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┤
│ 5 │ 2 │ 2 │ 2 │ 3 │ 4 │
├───┼───┼───┼───┼───┼───┤
│ 4 │ 5 │ 1 │ 6 │ 6 │ 7 │
└───┴───┴───┴───┴───┴───┘

P2 board verified.
Hash commit=1960830448338162390348349656925201022571500309579263256742339515213533721675field
p1 is starting turn now!


┌───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 4 │ 5 │ 3 │ 4 │
├───┼───┼───┼───┼───┼───┤
│ 2 │ 2 │ 5 │ 6 │ 6 │ 7 │
├───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┤
│ X │ X │ X │ X │ X │ X │
├───┼───┼───┼───┼───┼───┤
│ X │ X │ X │ X │ X │ X │
└───┴───┴───┴───┴───┴───┘

Please indicate which piece to move:
row: 1
column: 0
new row: 2
new column: 0
Player board verified.
New hash commit=1468645310925225490657405982157285187708398193353712892303552439212303809014field
p2 is starting turn now!


┌───┬───┬───┬───┬───┬───┐
│ X │ X │ X │ X │ X │ X │
├───┼───┼───┼───┼───┼───┤
│   │ X │ X │ X │ X │ X │
├───┼───┼───┼───┼───┼───┤
│ X │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┤
│ 5 │ 2 │ 2 │ 2 │ 3 │ 4 │
├───┼───┼───┼───┼───┼───┤
│ 4 │ 5 │ 1 │ 6 │ 6 │ 7 │
└───┴───┴───┴───┴───┴───┘

Please indicate which piece to move:
row: 4
column: 5
new row: 3
new column: 5
Player board verified.
New hash commit=3568700823377281081248679351191293413206805514813548872461011266183704765555field
p1 is starting turn now!


┌───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 4 │ 5 │ 3 │ 4 │
├───┼───┼───┼───┼───┼───┤
│   │ 2 │ 5 │ 6 │ 6 │ 7 │
├───┼───┼───┼───┼───┼───┤
│ 2 │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │ X │
├───┼───┼───┼───┼───┼───┤
│ X │ X │ X │ X │ X │   │
├───┼───┼───┼───┼───┼───┤
│ X │ X │ X │ X │ X │ X │
└───┴───┴───┴───┴───┴───┘
```

</details>

## Next steps
We recognize that there have been issues with the faucet and the testnet itself. Once these issues are resolved (and when we get access to some testnet credits 🙂), the program will be deployed to the testnet.

## Build Guide

To compile this Aleo program, run:
```bash
aleo build
```
 

# Acknowledgements
* The logo was made on Canva, using "Black & White Minimalist Business Logo."
