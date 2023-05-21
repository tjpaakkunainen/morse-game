import re
from resource import MORSE_DICT as morse_chars

print("Hello! Translate Morse to normal, and vice versa. '.-' becomes 'A', and so forth. "
      "Inputs are case-insensitive. To exit, type 'stop'.")

while True:
    char = str(input('Input character: '))

    if re.search(r'stop', char, re.IGNORECASE):
        print("Bye!")
        break

    char = char.upper()

    try:
        print(morse_chars[char])
    except KeyError:
        if char in morse_chars.values():
            ch_index = list(morse_chars.values()).index(char)
            print(list(enumerate(morse_chars.keys()))[ch_index][1])
        else:
            print(f"Input '{char}' not found")

