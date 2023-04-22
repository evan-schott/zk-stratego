
a = (2**(3*24+0) + 2**(3*24+1) + 2**(3*24+2))
print("og: "+ str(a))
# print("xx: " + str(7*2**(3*24+0)))

big = 318631593350490860862688876036096

for i in range(36):
    if (i == 35):
        b = 2**(3*i+0) + 2**(3*i+1) + 2**(3*i+2)
        print(b)
        c = b & big
        print(c)
        d = c >> (i*3)
        print(d)
    # if (i == 24):
    #     print(7*a)



# let mask: u128 = 2u128.pow(3u8*i) + 2u128.pow(3u8*i+1u8) + 2u128.pow(3u8*i+2u8); // ...000111000...
#             let cur_slot_raw: u128 = mask.and(board); 
#             assert(cur_slot_raw <= board);
#             let cur_slot: u128 = cur_slot_raw.shr_wrapped(i);
#             assert(cur_slot < 8u128);
