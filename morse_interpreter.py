import re
from resource import (MORSE_ALL as morse_all_chars,
                      MORSE_ALPHABET as morse_letters,
                      MORSE_NUMS as morse_nums,
                      MORSE_SPECIALS as morse_specials)

print("Hello! Translate Morse to normal, and vice versa. '.-' becomes 'A', and so forth. "
      "Inputs are case-insensitive. To exit, type 'stop'.")

while True:
    char = str(input('Input character: '))

    if re.search(r'stop', char, re.IGNORECASE):
        print("Bye!")
        break

    char = char.upper()

    try:
        print(morse_all_chars[char])
    except KeyError:
        if char in morse_all_chars.values():
            ch_index = list(morse_all_chars.values()).index(char)
            print(list(enumerate(morse_all_chars.keys()))[ch_index][1])
        else:
            print(f"Input '{char}' not found")

