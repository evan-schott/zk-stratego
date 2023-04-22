// The 'stratego' program.
program stratego.aleo {
    
    struct Board {
        r0: u8,
        r1: u8,
        r2: u8,
        r3: u8,
        r4: u8,
        r5: u8,
        r6: u8,
        r7: u8,
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
