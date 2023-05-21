from resource import MORSE_DICT as morse_chars

while True:
    char = str(input('character: '))

    if char == "stop":
        break

    char = char.upper()

    try:
        print(morse_chars[char])
    except KeyError:
        if char in morse_chars.values():
            ch_index = list(morse_chars.values()).index(char)
            print(list(enumerate(morse_chars.keys()))[ch_index][1])
        else:
            print(f"key '{char}' not found")

