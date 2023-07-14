from pynput import keyboard
from threading import Timer
import time


THRESHOLD = 0.3

def main():
    def on_key_press(key = None):
        return False

    def on_key_release(key = None):
        if input_round:
            input_round.cancel()

        time_pressed = round(time.time() - t, 2)

        input_chars.append("-") if time_pressed > THRESHOLD else input_chars.append(".")

        return False

    def parse_char(input_chars: list):
        cleaned = " ".join(input_chars)
        print()
        print(cleaned)
        input_chars.clear()

    input_round = None
    input_chars = []

    while True:
        with keyboard.Listener(on_press=on_key_press) as press_listener:
            press_listener.join()

        t = time.time()

        with keyboard.Listener(on_release=on_key_release) as release_listener:
            release_listener.join()

        input_round = Timer(1.5, parse_char, args=(input_chars,))
        input_round.start()

if __name__ == "__main__":
    main()
