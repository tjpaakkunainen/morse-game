import random
import re
from resource import (FAIL_MESSAGES as fail_messages,
                      MORSE_ALL as morse_all_chars,
                      MORSE_ALPHABET as morse_letters,
                      MORSE_NUMS as morse_nums,
                      MORSE_SPECIALS as morse_specials)

def morse_play():
    print("\nHello! Let's play a game. Try to guess what letter / number / special " 
          "character the morse code stands for. The game will try to keep your score "
          "(but won't store it anywhere)\n")
    
    score = 0

    while True:
        char_to_be_guessed = random.choice(list(morse_all_chars.keys()))
        print(char_to_be_guessed, end=" ")
        char = str(input())

        if re.search(r'stop', char, re.IGNORECASE):
            print(f"Your final score is {score}. Bye!")
            break

        if char.upper() == morse_all_chars[char_to_be_guessed]:
            score += 1
            print(f"Correct! Your score is {score}")
        else:
            print(f"{random.choice(fail_messages)} That was {morse_all_chars[char_to_be_guessed]}")