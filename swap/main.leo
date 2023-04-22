// The 'stratego' program.
program stratego.aleo {
    
    struct Board {
        r0: u128,
        r1: u128,
        r2: u128,
        r4: u128,
        r5: u128,
        r6: u128,
        r7: u128,
        r8: u128,
        r9: u128,
    }


    /*
    |----|----|----|----|----|----|----|----|----|----| 
    | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 |
    |----|----|----|----|----|----|----|----|----|----|
    | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 |
    |----|----|----|----|----|----|----|----|----|----|
    | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 |
    |----|----|----|----|----|----|----|----|----|----|
    | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 |
    |----|----|----|----|----|----|----|----|----|----|
    | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 |
    |----|----|----|----|----|----|----|----|----|----|
    | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 |
    |----|----|----|----|----|----|----|----|----|----|
    | 00 | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 |
    |----|----|----|----|----|----|----|----|----|----|
    | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 |
    |----|----|----|----|----|----|----|----|----|----|
    | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 |
    |----|----|----|----|----|----|----|----|----|----|
    | 30 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 |
    |----|----|----|----|----|----|----|----|----|----|   
    */
    struct Input {
        p0: u128,
        p1: u128,
        p2: u128,
        p3: u128,
        p4: u128,
        p5: u128,
        p6: u128,
        p7: u128,
        p8: u128,
        p9: u128,
        p10: u128,
        p11: u128,
        p12: u128,
        p13: u128,
        p14: u128,
        p15: u128,
    }




    transition init_p1(board: u128, seed: u128) -> field {

        // Count variables
        let c0: u8 = 0u8;
        let c1: u8 = 0u8;
        let c2: u8 = 0u8;
        let c3: u8 = 0u8;
        let c4: u8 = 0u8;
        let c5: u8 = 0u8;
        let c6: u8 = 0u8;
        let c7: u8 = 0u8;

        // Scan through pieces on board
        for i:u8 in 0u8..35u8 {
            
            let mask: u128 = 1u128.shl_wrapped(i) + 1u128.shl_wrapped(i+1u8) + 1u128.shl_wrapped(i+2u8); // ...000111000...
            let cur_slot_raw: u128 = mask.and(board); 
            assert(cur_slot_raw <= board);
            let cur_slot: u128 = cur_slot_raw.shr_wrapped(i);
            assert(cur_slot < 8u128);

            // Make sure only placing pieces on their side of board
            if i < 23u8 {
                assert(cur_slot == 0u128);
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

        // Check that placed appropriate number of pieces
        // assert(c0 == 24u8); // 24 blank spaces
        // assert(c1 == 1u8);  // 1 flag
        // assert(c2 == 3u8);  // 3 hash puzzles
        // assert(c3 == 1u8);  // 1 Whistleblower
        // assert(c4 == 2u8);  // 2 Inters
        // assert(c5 == 2u8);  // 2 Miners
        // assert(c6 == 2u8);  // 2 Devs
        // assert(c7 == 1u8);  // 1 CEO

        // Return hash commitment
        return Poseidon2::hash(board + seed);
    }

}
