import math

def md5_from_scratch(message):
    # --- HELPER FUNCTIONS ---
    def left_rotate(x, amount):
        x &= 0xFFFFFFFF
        return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

    # --- STEP 1: INITIALIZATION ---
    # MD5 uses 4 32-bit words as the initial buffer
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476

    # Round constants derived from the sine function
    K = [int(abs(math.sin(i + 1)) * (2**32)) & 0xFFFFFFFF for i in range(64)]

    # Per-round shift amounts
    S = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4

    # --- STEP 2: PREPROCESSING (PADDING) ---
    msg_bytes = bytearray(message, 'utf-8')
    orig_len_bits = (len(msg_bytes) * 8) & 0xFFFFFFFFFFFFFFFF

    print(f" Initializing MD5...")
    print(f"Original Message: {message}")

    # 2a. Append '1' bit (0x80)
    msg_bytes.append(0x80)

    # 2b. Pad with '0' until length is 448 bits modulo 512
    while (len(msg_bytes) * 8) % 512 != 448:
        msg_bytes.append(0x00)

    # 2c. Append 64-bit length (Little-endian for MD5)
    msg_bytes += orig_len_bits.to_bytes(8, 'little')

    total_bits = len(msg_bytes) * 8
    print(f"Total Block Size: {total_bits} bits")
    print(f"Padded Data (hex): {msg_bytes.hex()}")
    print("-" * 50)

    # --- STEP 3: PROCESS BLOCKS ---
    for i in range(0, len(msg_bytes), 64):
        chunk = msg_bytes[i:i+64]
        M = [int.from_bytes(chunk[j:j+4], 'little') for j in range(0, 64, 4)]

        AA, BB, CC, DD = A, B, C, D

        # 64 Rounds divided into 4 rounds of 16 operations each
        for j in range(64):
            if 0 <= j <= 15:
                f = (BB & CC) | ((~BB) & DD)
                g = j
            elif 16 <= j <= 31:
                f = (DD & BB) | ((~DD) & CC)
                g = (5 * j + 1) % 16
            elif 32 <= j <= 47:
                f = BB ^ CC ^ DD
                g = (3 * j + 5) % 16
            elif 48 <= j <= 63:
                f = CC ^ (BB | (~DD))
                g = (7 * j) % 16

            to_rotate = (AA + f + K[j] + M[g]) & 0xFFFFFFFF
            new_B = (BB + left_rotate(to_rotate, S[j])) & 0xFFFFFFFF

            AA, DD, CC, BB = DD, CC, BB, new_B

            # Print round trace for specific steps
            if j % 16 == 0:
                print(f"Round {j:02d} | A={AA:08x} B={BB:08x} C={CC:08x} D={DD:08x}")

        # Add result to the initial buffer
        A = (A + AA) & 0xFFFFFFFF
        B = (B + BB) & 0xFFFFFFFF
        C = (C + CC) & 0xFFFFFFFF
        D = (D + DD) & 0xFFFFFFFF
        print(f"Intermediate Hash: {A:08x}{B:08x}{C:08x}{D:08x}")

    # --- STEP 4: OUTPUT ---
    # Format as little-endian hexadecimal
    final_res = sum([x << (32 * i) for i, x in enumerate([A, B, C, D])])
    return hex(final_res)[2:].zfill(32)

# Execution
print("-" * 50)
print(f"FINAL MD5 HASH: {md5_from_scratch('good')}")
