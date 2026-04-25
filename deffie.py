def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
print("=== Diffie-Hellman Key Exchange ===")
# Public values
p = int(input("Enter a prime number (p): "))
g = int(input("Enter a primitive root (g): "))
# Validate prime
if not is_prime(p):
    print("Error: p must be a prime number!")
    exit()
# Private keys
a = int(input("Enter private key for User A: "))
b = int(input("Enter private key for User B: "))
# Compute public keys
A = pow(g, a, p)  # g^a mod p
B = pow(g, b, p)  # g^b mod p
print("\nPublic key of A:", A)
print("Public key of B:", B)
# Compute shared secret keys
key_A = pow(B, a, p)
key_B = pow(A, b, p)
print("\nSecret key computed by A:", key_A)
print("Secret key computed by B:", key_B)
# Verify
if key_A == key_B:
    print("\nShared Secret Key Established Successfully!")
else:
    print("\nError in key exchange!")
