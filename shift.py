def encrypt(text, shift):
    result = ""

    for char in text:
        if char.isalpha():
            # Check if uppercase or lowercase
            if char.isupper():
                result += chr((ord(char) + shift - 65) % 26 + 65)
            else:
                result += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            result += char  # Keep spaces and symbols unchanged

    return result


# Function to decrypt text
def decrypt(text, shift):
    return encrypt(text, -shift)


# Main program
text = input("Enter the message: ")
shift = int(input("Enter shift value: "))

encrypted = encrypt(text, shift)
print("Encrypted text:", encrypted)

decrypted = decrypt(encrypted, shift)
print("Decrypted text:", decrypted)
OUTPUT:
Enter the message: A SECRET KEY
Enter shift value: 5
Encrypted text: F XJHWJY PJD
Decrypted text: A SECRET KEY
