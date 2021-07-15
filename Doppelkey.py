import mouse
import keyboard
import time
import threading

mrep = 1
krep = 1
speed = 1

def keyplay(krep, num, speed):
    while (krep <= num):
        keyboard.play(keyboard_events, speed_factor=speed)
        krep += 1

def mouseplay(mrep, num, speed):
    while (mrep <= num):
        mouse.play(mouse_events, include_wheel=True, include_clicks=True, speed_factor=speed)
        mrep += 1

while (True):
    num = input("Number of repeats:\n")
    if (num.isdigit):
        num = int(num)
        if (num <= 50):
            break
        if (num > 50):
            print("The number you've chosen is over 50, are you certain this number is correct and not too high?\n")
            if (input("You can still cancel now, to cancel press 'C' if not, press any other key:\n").lower() == "c"):
                pass
            else:
                break
    else:
        print("Invalid input, try again.")
        pass

print("Leave the replay speed empty to use default speed, just press enter.")
while (True):
    speed = input("Set the speed (Max of 40, default = 1):\n")
    if (speed == ""):
        speed = 1
        break
    if (speed.isdigit):
        speed = int(speed)
        if (speed <= 40):
            break
        if (speed > 40):
            print("Speed is set too high, please enter a speed below 40.\n")
            pass
    else:
        print("Invalid input, try again.")
        pass
print("Press f8 to start recording, and press f8 again to stop recording.")

mouse_events = []

keyboard.wait("f8")
print("start")
mouse.hook(mouse_events.append)
keyboard.start_recording()

keyboard.wait("f8")
print("stop")
mouse.unhook(mouse_events.append)
keyboard_events = keyboard.stop_recording()

print("Press f7 to replay the recording.")
keyboard.wait("f7")
time.sleep(1)

keyplaythread = threading.Thread(target=lambda :keyplay(krep, num, speed))
mouseplaythread = threading.Thread(target=lambda :mouseplay(mrep, num, speed))

keyplaythread.start()
mouseplaythread.start()

keyplaythread.join()
mouseplaythread.join()
print("done")