// The 'stratego' program.
program stratego.aleo {

    /** 
    * Moves/Removes a piece and produces a new commitment for the new board. 
    *
    * @param board the board before moving/removing the piece
    * @param salt the salt that was used to produce the hash commitment
    * @param hash public hash commitment to the board 
    * @param x1 initial x position of the piece
    * @param y1 initial y position of the piece
    * @param x2 final x position of the piece. if the piece gets removed, this parameter does not affect anything
    * @param y2 final y position of the piece. if the piece gets removed, this parameter does not affect anything
    * @param is_killed true if the piece is getting removed.
    * @return hash commitment to the new board
    * 
    * When a player's piece configuration changes, the commitment to their old board is no longer relevant. So,
    * they need to generate a new one. A piece configuration can change if 1) a piece simply gets moved, 2) a piece
    * gets attacked by a stronger piece and killed, 3) a piece tries to attack a stronger piece but gets killed,
    * 4) a piece attacks a weaker piece and replaced it on the board. This function proves that the board being updated
    * is the board representing the last state of the piece configuration before the update. It then moves or removes the
    * relevant piece on/from the board as necessary.
    **/
    transition update_state(board: u128, salt: u128, public hash: field, public x1: u8, public y1: u8, public x2: u8, public y2: u8, public is_killed: bool) -> field {
        // we need to be revealing a position on the board that we had committed to
        assert_eq(Poseidon2::hash(board + salt), hash);

        // note that we are not checking that the coordinates are on the board.
        // because the coordinates are public, the opponent can simply reject 
        // the proof if silly coordinates were provided. this is not a zk issue.

        let new_board: u128 = 0u128;
        let i: u8 = 6u8*x1 + y1;
        let mask: u128 = 2u128.pow(3u8*i) + 2u128.pow(3u8*i+1u8) + 2u128.pow(3u8*i+2u8);
        let val: u128 = mask.and(board);
        
        // Delete position (x,y)
        new_board = board - val;

        // Case you are executing normal move, or have won combat
        if is_killed.not() { 

            // prove didn't move bomb or flag 
            assert_neq(val, 2u128);
            assert_neq(val, 1u128);

            // figure out strength value of piece
            let strength: u128 = val.shr_wrapped(i*3u8);

            // figure out what value to add
            let i2: u8 = 6u8*x2 + y2;
            new_board += strength * (2u128.pow(3u8*i2));
        }

        return Poseidon2::hash(new_board + salt);
    }


    /** 
    * Reveals the piece in the given coordinate. 
    *
    * @param board the board before removing the piece
    * @param salt the salt that was used to produce the hash commitment
    * @param hash public hash commitment to the board
    * @param x x position of the piece
    * @param y y position of the piece
    * @return the type of the piece at position (x,y)
    * 
    * When a piece attacks/gets attacked by another piece, both players need to announce the types
    * of their pieces. The strengths of the pieces then get compared. This function reveals the type
    * of the piece in the given location while proving that it is using the most recent state of the 
    * board. Note that this function does not do any bound checks for the position: because the location
    * is public, the prover must input meaningful positions. Otherwise, the opponent will not get convinced.
    *  If the location was private, we would have had to do bound checks.
    **/
    transition reveal_piece(board: u128, salt: u128, public hash: field, public x: u8, public y: u8) -> u128 {
        // cannot reveal a position outside the board
        
        // we need to be revealing a position on the board that we had committed to
        assert_eq(Poseidon2::hash(board + salt), hash);
        let i: u8 = 6u8*x + y;
        let mask: u128 = 2u128.pow(3u8*i) + 2u128.pow(3u8*i+1u8) + 2u128.pow(3u8*i+2u8);
        let val: u128 = mask.and(board);
        let ret: u128 = val.shr_wrapped(i*3u8);

        return ret;
    }

    /** 
    * Produces a hash commitment to the board.
    *
    * @param board the board before moving/removing the piece
    * @param salt the salt that was used to produce the hash commitment
    * @param is_player_2 true if this is the 
    * @return hash commitment to the board
    * 
    * Each player needs to assure their opponent that the way they place their piece on the board is valid.
    * However, they are not supposed to reveal which piece is where. In other words, for every position on 
    * the board, the opponent should only know whether there is a piece there or not. They shouldn't learn
    * the type of the piece. This function produces a hash that acts as a commitment to the piece configuration.
    * When making the next move, this hash value is referenced to prove that no piece has been sneakily moved
    * since the last public move.
    **/
    transition commit_board(board: u128, salt: u128, is_player_2: bool) -> public field {

        // counters for the pieces
        let c0: u8 = 0u8;
        let c1: u8 = 0u8;
        let c2: u8 = 0u8;
        let c3: u8 = 0u8;
        let c4: u8 = 0u8;
        let c5: u8 = 0u8;
        let c6: u8 = 0u8;
        let c7: u8 = 0u8;

        // Scan through pieces on board
        for i:u8 in 0u8..36u8 {
            
            let mask: u128 = 2u128.pow(3u8*i) + 2u128.pow(3u8*i+1u8) + 2u128.pow(3u8*i+2u8); // ...000111000...
            let cur_slot_raw: u128 = mask.and(board); 
            assert(cur_slot_raw <= board);
            let cur_slot: u128 = cur_slot_raw.shr_wrapped(i*3u8);
            assert(cur_slot < 8u128);

            // Make sure only placing pieces on their side of board
            if is_player_2 {
                if i < 24u8 {
                    assert(cur_slot == 0u128);
                }
                if i >= 24u8 {
                    assert(cur_slot > 0u128);
                }
            } else {
                if i >= 24u8 {
                    assert(cur_slot == 0u128);
                }
                if i < 12u8 {
                    assert(cur_slot > 0u128);
                }
            }

            // Tally up pieces
            if cur_slot == 0u128 {
                c0 += 1u8;
            }
            if cur_slot == 1u128 {
                c1 += 1u8;
            }
            if cur_slot == 2u128 {
                c2 += 1u8;
            }
            if cur_slot == 3u128 {
                c3 += 1u8;
            }
            if cur_slot == 4u128 {
                c4 += 1u8;
            }
            if cur_slot == 5u128 {
                c5 += 1u8;
            }
            if cur_slot == 6u128 {
                c6 += 1u8;
            }
            if cur_slot == 7u128 {
                c7 += 1u8;
            }
        }

        // check that placed appropriate number of pieces
        assert(c0 == 24u8); // 24 blank spaces
        assert(c1 == 1u8);  // 1 flag
        assert(c2 == 3u8);  // 3 hash puzzles
        assert(c3 == 1u8);  // 1 Whistleblower
        assert(c4 == 2u8);  // 2 Interns
        assert(c5 == 2u8);  // 2 Miners
        assert(c6 == 2u8);  // 2 Devs
        assert(c7 == 1u8);  // 1 CEO

        // Return hash commitment
        return Poseidon2::hash(board + salt);
    }
}
