def get_minor(matrix, i, j):
    return [row[:j] + row[j+1:] for row in (matrix[:i] + matrix[i+1:])]


# Function to compute determinant
def determinant(matrix):
    if len(matrix) == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]

    det = 0
    for c in range(len(matrix)):
        det += ((-1)**c) * matrix[0][c] * determinant(get_minor(matrix, 0, c))
    return det


# Function to find modular inverse
def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


# Function to find adjoint of matrix
def adjoint(matrix):
    n = len(matrix)
    adj = [[0]*n for _ in range(n)]

    if n == 2:
        adj[0][0] = matrix[1][1]
        adj[0][1] = -matrix[0][1]
        adj[1][0] = -matrix[1][0]
        adj[1][1] = matrix[0][0]
        return adj

    for i in range(n):
        for j in range(n):
            sign = (-1) ** (i + j)
            minor = get_minor(matrix, i, j)
            adj[j][i] = sign * determinant(minor)

    return adj


# Function to find inverse matrix mod 26
def inverse_matrix(matrix):
    det = determinant(matrix)
    det_mod = det % 26

    inv_det = mod_inverse(det_mod, 26)
    if inv_det is None:
        print(“ Matrix not invertible mod 26")
        return None

    adj = adjoint(matrix)
    n = len(matrix)
    inv = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            inv[i][j] = (adj[i][j] * inv_det) % 26

    return inv


# Function for matrix multiplication
def matrix_multiply(mat, vec):
    result = []
    for row in mat:
        sum_val = 0
        for i in range(len(vec)):
            sum_val += row[i] * vec[i]
        result.append(sum_val % 26)
    return result


# Convert text to numbers
def text_to_numbers(text):
    return [ord(c) - 65 for c in text]


# Convert numbers to text
def numbers_to_text(nums):
    return ''.join(chr(n + 65) for n in nums)


# Encrypt function
def encrypt(text, key_matrix):
    text = text.replace(" ", "").upper()
    n = len(key_matrix)

    # Padding
    while len(text) % n != 0:
        text += 'X'

    result = ""

    for i in range(0, len(text), n):
        block = text[i:i+n]
        vec = text_to_numbers(block)
        enc = matrix_multiply(key_matrix, vec)
        result += numbers_to_text(enc)

    return result


# Decrypt function
def decrypt(cipher, key_matrix):
    inv_matrix = inverse_matrix(key_matrix)
    if inv_matrix is None:
        return None

    n = len(inv_matrix)
    result = ""

    for i in range(0, len(cipher), n):
        block = cipher[i:i+n]
        vec = text_to_numbers(block)
        dec = matrix_multiply(inv_matrix, vec)
        result += numbers_to_text(dec)

    return result

def get_key_matrix():
    n = int(input("Enter size of key matrix (n): "))
    print("Enter the key matrix row-wise:")

    key_matrix = []
    for i in range(n):
        row = list(map(int, input().split()))

        if len(row) != n:
            print(" Invalid row length!")
            exit()

        key_matrix.append(row)

    # Check invertibility
    det = determinant(key_matrix) % 26
    if mod_inverse(det, 26) is None:
        print(" Invalid key! Not invertible mod 26")
        exit()

    return key_matrix


# ================= MAIN =================
print("=== Hill Cipher ===")

key_matrix = get_key_matrix()

text = input("Enter message: ")

cipher = encrypt(text, key_matrix)
print("Encrypted:", cipher)

plain = decrypt(cipher, key_matrix)
print("Decrypted:", plain)
