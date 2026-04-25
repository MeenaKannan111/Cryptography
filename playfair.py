def clean(text):
    return ''.join(c for c in text.upper() if c.isalpha()).replace('J', 'I')

def build_grid(key):
    key = clean(key)
    seen = set()
    letters = []

    # Add key letters first
    for ch in key:
        if ch not in seen:
            seen.add(ch)
            letters.append(ch)

    # Add remaining alphabets (without J)
    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in seen:
            seen.add(ch)
            letters.append(ch)

    # 5x5 grid
    grid = [letters[i:i+5] for i in range(0, 25, 5)]
    return grid


def find(grid, ch):
    for i in range(5):
        for j in range(5):
            if grid[i][j] == ch:
                return i, j
    return None


def prepare(text):
    text = clean(text)
    res = []
    i = 0

    while i < len(text):
        a = text[i]

        if i+1 < len(text):
            b = text[i+1]

            if a == b:
                res.append((a, 'X'))
                i += 1
            else:
                res.append((a, b))
                i += 2
        else:
            res.append((a, 'X'))
            i += 1

    return res


def playfair():
    print("=== Playfair Cipher ===")

    key = input("Keyword: ")
    text = input("Plaintext: ")

    grid = build_grid(key)

    #  Print Grid
    print("\nGrid:")
    for row in grid:
        print(' '.join(row))

    pairs = prepare(text)
    print("\nPairs:", pairs)

    cipher = ""

    #  Encryption
    for a, b in pairs:
        pos1 = find(grid, a)
        pos2 = find(grid, b)

        if pos1 is None or pos2 is None:
            print("Error: character not found")
            return

        r1, c1 = pos1
        r2, c2 = pos2

        if r1 == r2:
            cipher += grid[r1][(c1+1) % 5] + grid[r2][(c2+1) % 5]
        elif c1 == c2:
            cipher += grid[(r1+1) % 5][c1] + grid[(r2+1) % 5][c2]
        else:
            cipher += grid[r1][c2] + grid[r2][c1]

    print("\nEncrypted:", cipher)

    # Decryption
    decrypted = ""

    for i in range(0, len(cipher), 2):
        a, b = cipher[i], cipher[i+1]

        r1, c1 = find(grid, a)
        r2, c2 = find(grid, b)

        if r1 == r2:
            decrypted += grid[r1][(c1-1) % 5] + grid[r2][(c2-1) % 5]
        elif c1 == c2:
            decrypted += grid[(r1-1) % 5][c1] + grid[(r2-1) % 5][c2]
        else:
            decrypted += grid[r1][c2] + grid[r2][c1]

    print("Decrypted:", decrypted)

playfair()
