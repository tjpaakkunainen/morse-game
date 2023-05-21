import morse_play
import morse_practice
import re

print("\nWelcome to (probably) the most rudimental morse program you've ever played. "
      "You can either practice morse, or play a morse guessing game."
      "\n")

while True:
    cmd = str(input("What to do? (practice / play / quit) "))

    if re.search(r'quit', cmd, re.IGNORECASE):
        print("Thanks for trying! Bye!")
        break

    if cmd.lower() == "play":
        morse_play.morse_play()

    elif cmd.lower() == "practice":
        morse_practice.morse_practice()

    else:
        print("\nDidn't quite catch that. Valid options are practice, play and quit. Let's try again.\n")
