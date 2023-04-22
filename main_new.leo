// The 'stratego' program.
program stratego.aleo {

    struct Board {
        r1: Row,
        r2: Row,
        r3: Row,
        r4: Row,
        r5: Row,
        r6: Row,
        r7: Row,
        r8: Row,
        r9: Row,
        r10: Row
    }

    struct Row {
        c1: u8,
        c2: u8,
        c3: u8,
        c4: u8,
        c5: u8,
        c6: u8,
        c7: u8,
        c8: u8,
        c9: u8,
        c10: u8
    }

    transition commit_to_board(board: Board, seed: u128) -> field {
        
        // Count variables
        let c0: u8 = 0u8;
        let c1: u8 = 0u8;
        let c2: u8 = 0u8;
        let c3: u8 = 0u8;
        let c4: u8 = 0u8;
        let c5: u8 = 0u8;
        let c6: u8 = 0u8;
        let c7: u8 = 0u8;
        
        // check that no piece was placed beyond the 4. row from the bottom
        assert(board.r1.c1 == 0u8);
        assert(board.r1.c2 == 0u8);
        assert(board.r1.c3 == 0u8);
        assert(board.r1.c4 == 0u8);
        assert(board.r1.c5 == 0u8);
        assert(board.r1.c6 == 0u8);
        assert(board.r1.c7 == 0u8);
        assert(board.r1.c8 == 0u8);
        assert(board.r1.c9 == 0u8);
        assert(board.r1.c10 == 0u8);
        assert(board.r2.c1 == 0u8);
        assert(board.r2.c2 == 0u8);
        assert(board.r2.c3 == 0u8);
        assert(board.r2.c4 == 0u8);
        assert(board.r2.c5 == 0u8);
        assert(board.r2.c6 == 0u8);
        assert(board.r2.c7 == 0u8);
        assert(board.r2.c8 == 0u8);
        assert(board.r2.c9 == 0u8);
        assert(board.r2.c10 == 0u8);
        assert(board.r1.c1 == 0u8);
        assert(board.r1.c2 == 0u8);
        assert(board.r1.c3 == 0u8);
        assert(board.r1.c4 == 0u8);
        assert(board.r1.c5 == 0u8);
        assert(board.r1.c6 == 0u8);
        assert(board.r1.c7 == 0u8);
        assert(board.r1.c8 == 0u8);
        assert(board.r1.c9 == 0u8);
        assert(board.r1.c10 == 0u8);


        // Scan through pieces on board
        for i:u8 in 0u8..35u8 {
            
            let mask: u128 = 2u128.pow(3u8*i) + 2u128.pow(3u8*i+1u8) + 2u128.pow(3u8*i+2u8); // ...000111000...
            let cur_slot_raw: u128 = mask.and(board); 
            assert(cur_slot_raw <= board);
            let cur_slot: u128 = cur_slot_raw.shr_wrapped(i);
            assert(cur_slot < 8u128);

            // Make sure only placing pieces on their side of board
            // if i < 24u8 {
            //     assert(cur_slot == 0u128);
            // }
            // if i == 24u8 {
            //     assert(cur_slot > 0u128);
            // }

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

        //Check that placed appropriate number of pieces
        // assert(c0 == 24u8); // 24 blank spaces
        // assert(c1 == 1u8);  // 1 flag
        // assert(c2 == 3u8);  // 3 hash puzzles
        // assert(c3 == 0u8);  // 1 Whistleblower
        // assert(c4 == 0u8);  // 2 Inters
        // assert(c5 == 0u8);  // 2 Miners
        // assert(c6 == 0u8);  // 2 Devs
        //assert(c7 == 1u8);  // 1 CEO

        // Return hash commitment
        return Poseidon2::hash(board + seed);
    }

}
