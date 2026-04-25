import struct

# --- 1. AES CORE ENGINE (From Scratch) ---
SBOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

RCON = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

def xtime(a):
    return (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

def aes_key_expansion(key):
    w = [list(key[i:i+4]) for i in range(0, 16, 4)]
    for i in range(4, 44):
        temp = w[i-1][:]
        if i % 4 == 0:
            temp = temp[1:] + temp[:1]
            temp = [SBOX[b] for b in temp]
            temp[0] ^= RCON[i//4]
        w.append([w[i-4][j] ^ temp[j] for j in range(4)])
    return [b for word in w for b in word]

def aes_encrypt_block_with_rounds(block, rk, label):
    state = list(block)
    print(f"\n--- [AES ROUNDS FOR {label}] ---")
    print(f"Input Data:      {bytes(state).hex()}")
    for i in range(16): state[i] ^= rk[i]
    print(f"Round 0 (ARK):   {bytes(state).hex()}")
    for r in range(1, 10):
        state = [SBOX[b] for b in state]
        state = [state[0], state[5], state[10], state[15], state[4], state[9], state[14], state[3],
                 state[8], state[13], state[2], state[7], state[12], state[1], state[6], state[11]]
        for i in range(0, 16, 4):
            s0, s1, s2, s3 = state[i:i+4]
            t = s0 ^ s1 ^ s2 ^ s3
            state[i] ^= t ^ xtime(s0 ^ s1); state[i+1] ^= t ^ xtime(s1 ^ s2)
            state[i+2] ^= t ^ xtime(s2 ^ s3); state[i+3] ^= t ^ xtime(s3 ^ s0)
        for i in range(16): state[i] ^= rk[r*16 + i]
        print(f"Round {r}:         {bytes(state).hex()}")
    state = [SBOX[b] for b in state]
    state = [state[0], state[5], state[10], state[15], state[4], state[9], state[14], state[3],
             state[8], state[13], state[2], state[7], state[12], state[1], state[6], state[11]]
    for i in range(16): state[i] ^= rk[160 + i]
    print(f"Round 10 (Final): {bytes(state).hex()}")
    return bytes(state)

# --- 2. CMAC LOGIC ---
def left_shift(data):
    res = bytearray(16); overflow = 0
    for i in range(15, -1, -1):
        new_ov = (data[i] >> 7) & 1
        res[i] = ((data[i] << 1) | overflow) & 0xFF
        overflow = new_ov
    return bytes(res)

def xor_bytes(a, b): return bytes(x ^ y for x, y in zip(a, b))

def aes_cmac_detailed(key_bytes, msg):
    print("\n--- [STEP 1: PREPROCESSING & PADDING] ---")
    n = (len(msg) + 15) // 16
    complete = (len(msg) > 0 and len(msg) % 16 == 0)
    
    # Show the padding at the start
    if not complete:
        M_last_temp = msg[(n-1)*16:]
        padded_msg_view = M_last_temp + b'\x80' + b'\x00' * (15 - len(M_last_temp))
        print(f"Original Message: {msg.decode()}")
        print(f"Padded Final Block: {padded_msg_view.hex()}")
    else:
        print(f"Original Message: {msg.decode()}")
        print("Message is a complete block, no padding needed.")

    print("\n--- [STEP 2: KEY EXPANSION] ---")
    rk = aes_key_expansion(key_bytes)
    print(f"Master Key: {key_bytes.hex()}")

    print("\n--- [STEP 3: SUBKEY GENERATION] ---")
    L = aes_encrypt_block_with_rounds(bytes(16), rk, "SUBKEY GEN (L)")
    print(f"\nValue of L (AES_K(0)): {L.hex()}")

    def get_k(val, name):
        msb = (val[0] >> 7) & 1
        shifted = left_shift(val)
        if msb == 0:
            res = shifted
            print(f"{name} Logic: Shift Left (MSB was 0)")
        else:
            res = bytes(shifted[i] ^ (0x87 if i == 15 else 0) for i in range(16))
            print(f"{name} Logic: Shift Left + XOR 0x87 (MSB was 1)")
        return res

    k1 = get_k(L, "K1"); print(f"K1: {k1.hex()}")
    k2 = get_k(k1, "K2"); print(f"K2: {k2.hex()}")

    print("\n--- [STEP 4: CBC CHAINING] ---")
    X = bytes(16)
    for i in range(n - 1):
        print(f"\nProcessing Intermediate Block {i+1}")
        X = aes_encrypt_block_with_rounds(xor_bytes(X, msg[i*16:(i+1)*16]), rk, f"BLOCK {i+1}")

    M_last = msg[(n-1)*16:]
    if complete:
        M_final = xor_bytes(M_last, k1)
        print(f"\nAction: XOR last block with K1")
    else:
        padded = M_last + b'\x80' + b'\x00' * (15 - len(M_last))
        M_final = xor_bytes(padded, k2)
        print(f"\nAction: XOR padded block with K2")

    tag = aes_encrypt_block_with_rounds(xor_bytes(X, M_final), rk, "FINAL TAG")
    return tag

# --- 3. EXECUTION ---
key = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
msg_input = input("Enter message: ").encode()
tag = aes_cmac_detailed(key, msg_input)
print(f"\nFINAL CMAC TAG: {tag.hex()}")
