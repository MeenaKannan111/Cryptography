def permute(bits, table):
    return [bits[i-1] for i in table]
def left_shift(bits, n):
    return bits[n:] + bits[:n]
def xor(a, b):
    return [i ^ j for i, j in zip(a, b)]
def sbox(bits, box):
    row = int(str(bits[0]) + str(bits[3]), 2)
    col = int(str(bits[1]) + str(bits[2]), 2)
    val = box[row][col]
    return [int(x) for x in format(val, '02b')]
S0 = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
S1 = [[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]
def generate_keys(key):
    k = permute(key, P10)
    L, R = k[:5], k[5:]
    L, R = left_shift(L,1), left_shift(R,1)
    K1 = permute(L+R, P8)
    L, R = left_shift(L,2), left_shift(R,2)
    K2 = permute(L+R, P8)
    return K1, K2
def fk(bits, key):
    L, R = bits[:4], bits[4:]
    temp = xor(permute(R, EP), key)
    left = sbox(temp[:4], S0)
    right = sbox(temp[4:], S1)
    return xor(L, permute(left+right, P4)) + R
def sdes_encrypt(pt, key):
    K1, K2 = generate_keys(key)
    ip = permute(pt, IP)
    r1 = fk(ip, K1)
    sw = r1[4:] + r1[:4]
    r2 = fk(sw, K2)
    return permute(r2, IP_INV)
def sdes_decrypt(cipher, key):
    K1, K2 = generate_keys(key)
    ip = permute(cipher, IP)
    r1 = fk(ip, K2)   # reverse order
    sw = r1[4:] + r1[:4]
    r2 = fk(sw, K1)
    return permute(r2, IP_INV)
# INPUT
pt  = [int(x) for x in input("Plaintext (8-bit): ")]
key = [int(x) for x in input("Key (10-bit): ")]
P10 = list(map(int, input("P10: ").split()))
P8  = list(map(int, input("P8: ").split()))
IP  = list(map(int, input("IP: ").split()))
IP_INV = list(map(int, input("IP-1: ").split()))
EP  = list(map(int, input("EP: ").split()))
P4  = list(map(int, input("P4: ").split()))
# Encrypt
cipher = sdes_encrypt(pt, key)
print("Cipher:", ''.join(map(str, cipher)))
# Decrypt (using same cipher)
plaintext = sdes_decrypt(cipher, key)
print("Decrypted Plaintext:", ''.join(map(str, plaintext)))
