def caesar():
    text = input("Plaintext: ").upper()
    shift = int(input("Shift: "))

    enc = ""
    for c in text:
        if c.isalpha():
            enc += chr((ord(c)-65+shift)%26 + 65)
        else:
            enc += c

    print("Encrypted:", enc)

    dec = ""
    for c in enc:
        if c.isalpha():
            dec += chr((ord(c)-65-shift)%26 + 65)
        else:
            dec += c

    print("Decrypted:", dec)

caesar()
