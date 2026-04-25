def generate_key(text, key):
    key = list(key)
    if len(text) == len(key):
        return key
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)


# Function to encrypt text
def encrypt(text, key):
    encrypted_text = ""
    key = generate_key(text, key)

    for i in range(len(text)):
        if text[i].isalpha():
            shift = ord(key[i].lower()) - 97
            if text[i].isupper():
                encrypted_text += chr((ord(text[i]) + shift - 65) % 26 + 65)
            else:
                encrypted_text += chr((ord(text[i]) + shift - 97) % 26 + 97)
        else:
            encrypted_text += text[i]

    return encrypted_text


# Function to decrypt text
def decrypt(cipher_text, key):
    decrypted_text = ""
    key = generate_key(cipher_text, key)

    for i in range(len(cipher_text)):
        if cipher_text[i].isalpha():
            shift = ord(key[i].lower()) - 97
            if cipher_text[i].isupper():
                decrypted_text += chr((ord(cipher_text[i]) - shift - 65) % 26 + 65)
            else:
                decrypted_text += chr((ord(cipher_text[i]) - shift - 97) % 26 + 97)
        else:
            decrypted_text += cipher_text[i]

    return decrypted_text


# Main program
text = input("Enter the message: ")
key = input("Enter the key: ")

encrypted = encrypt(text, key)
print("Encrypted text:", encrypted)

decrypted = decrypt(encrypted, key)
print("Decrypted text:", decrypted)
