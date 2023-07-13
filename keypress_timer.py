from pynput import keyboard 
import time

# WIP!!!!

def on_key_release(key): #what to do on key-release
    time_taken = round(time.time() - t, 2) #rounding the long decimal float
    # dfprint("The key",key," is pressed for",time_taken,'seconds')
    return time_taken #stop detecting more key-releases

def on_key_press(key): #what to do on key-press
    return False #stop detecting more key-presses



t = time.time() #reading time in sec
def main():
    print("hello!")
    with keyboard.Listener(on_press = on_key_press) as press_listener: #setting code for listening key-press
        press_listener.join()

    with keyboard.Listener(on_release = on_key_release) as release_listener: #setting code for listening key-release
        time = release_listener.join()
        print(time)

x = main()
print(x)

# WIP !!!