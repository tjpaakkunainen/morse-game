from pynput import keyboard
from threading import Timer, Event
from resource import MORSE_COMMON as morse_characters
import random
import time
import sys

THRESHOLD = 0.3

def play():

    def on_key_press(key = None):
        return False

    def on_key_release(key = None):
        if input_round:
            input_round.cancel()

        time_pressed = round(time.time() - t, 2)

        input_chars.append("-") if time_pressed > THRESHOLD else input_chars.append(".")

        return False

    def parse_char(input_chars: list, char_to_be_guessed: str):
 
        cleaned = "".join(input_chars)
        ch_index = list(morse_characters.values()).index(char_to_be_guessed)
        right_choice = list(enumerate(morse_characters.keys()))[ch_index][1]
        print()
        try:
            print(f"Your guess: {cleaned} which corresponds to: {morse_characters[cleaned]}")

            if morse_characters[cleaned] == char_to_be_guessed:
                print("Correct!", end=" ")

        except KeyError:
            print(f"Your guess: {cleaned} which I cannot fathom")
  
        finally:
            print(f"Right answer: {right_choice} ({char_to_be_guessed})")
            game_active.clear()
            input_chars.clear()
            time.sleep(0.5)
            print("\nPress enter to continue, ctrl+c to quit")
            time.sleep(0.5)
            sys.exit()

    input_round = None
    input_chars = []
    game_active = ["I can 'clear' a list to get False, but can't set variable to False, WHY"]

    char_to_be_guessed = random.choice(list(morse_characters.values()))
    print("What's this in morse: ", char_to_be_guessed)

    while True:
        with keyboard.Listener(on_press=on_key_press) as press_listener:
            press_listener.join()

        t = time.time()

        with keyboard.Listener(on_release=on_key_release) as release_listener:
            release_listener.join()

        if not game_active:
            break

        input_round = Timer(1.0, parse_char, args=(input_chars, char_to_be_guessed))
        input_round.daemon = True
        input_round.start()

def main():
    print("\nWelcome to morse game!\n\nYour spacebar is the key. Program gives you a character and you need to translate it to "
          "morse.\nShort press is dit ('.') and longer press is dah ('-'). Good luck! \n")
    first_time = True
    while True:
        if first_time:
            whatdo = input("Press enter to play, type y to quit: \n")
        else:
            whatdo = input()
        if "y" in whatdo:
            print("\nBye!")
            break
        else:
            play()
        first_time = False

if __name__ == "__main__":
    main()
