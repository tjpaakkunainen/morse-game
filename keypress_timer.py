from pynput import keyboard
from threading import Timer, Event
from resource import MORSE_ALL as morse_all_chars
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
        ch_index = list(morse_all_chars.values()).index(char_to_be_guessed)
        right_choice = list(enumerate(morse_all_chars.keys()))[ch_index][1]
        print()
        try:
            print(f"Your guess: {cleaned} which corresponds to: {morse_all_chars[cleaned]}")

            if morse_all_chars[cleaned] == char_to_be_guessed:
                print("Correct!", end=" ")

        except KeyError:
            print(f"Your guess: {cleaned} which I cannot fathom")
  
        finally:
            print(f"Right answer: {right_choice} ({char_to_be_guessed})")
            game_active.clear()
            input_chars.clear()
            time.sleep(1)
            print("press any key to continue")
            sys.exit()


    input_round = None
    input_chars = []
    game_active = ["yes"]

    char_to_be_guessed = random.choice(list(morse_all_chars.values()))
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
    while True:
        whatdo = input("wanna play? ")
        if "y" in whatdo:
            play()
        else:
            print("you commanded:", whatdo)
            print("quit!")
            break

if __name__ == "__main__":
    main()
