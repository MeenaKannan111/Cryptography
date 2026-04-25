def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
# Function to find modular inverse (Extended Euclidean Algorithm)
def mod_inverse(e, phi):
    t, new_t = 0, 1
    r, new_r = phi, e
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r
    if r > 1:
        return None
    if t < 0:
        t = t + phi
    return t
# Function for RSA key generation
def generate_keys():
    # Small prime numbers (for learning purpose)
    p = int(input("Enter prime number p: "))
    q = int(input("Enter prime number q: "))
    n = p * q
    phi = (p - 1) * (q - 1)
    # Choose e such that gcd(e, phi) = 1
    e = int(input("Enter value of e (1 < e < phi and gcd(e, phi)=1): "))
    while gcd(e, phi) != 1:
        print("Invalid e. Try again.")
        e = int(input("Enter value of e: "))
    # Compute d
    d = mod_inverse(e, phi)
    return (e, d, n, p, q)
# Function to encrypt
def encrypt(message, e, n):
    cipher = []
    for char in message:
        cipher.append(pow(ord(char), e, n))
    return cipher
# Function to decrypt
def decrypt(cipher, d, n):
    message = ""
    for num in cipher:
        message += chr(pow(num, d, n))
    return message
# -------- MAIN PROGRAM --------
print("=== RSA Algorithm ===")
e, d, n, p, q = generate_keys()
print("Public Key (n, e):", (n, e))
print("Private Key (p, q, d):", (p, q, d))
message = input("Enter message: ")
cipher = encrypt(message, e, n)
print("Encrypted message:", cipher)
decrypted = decrypt(cipher, d, n)
print("Decrypted message:", decrypted)
