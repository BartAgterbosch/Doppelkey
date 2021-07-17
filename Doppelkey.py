import mouse
import keyboard
import ctypes
from threading import Thread
from time import sleep
from sys import platform
from os import system

ctypes.windll.user32.SetProcessDPIAware()
if (platform == "win32"):
    clear = "cls"
else:
    clear = "clear"


while (True):
    rep = 1
    speed = 1

    
#Funtions
    def replay():
        if (keyboard.read_key() == "f7"):
            keyplaythread = Thread(target=lambda :keyplay(rep, num, speed))
            mouseplaythread = Thread(target=lambda :mouseplay(rep, num, speed, pos))

            keyplaythread.start()
            mouseplaythread.start()

            keyplaythread.join()
            mouseplaythread.join()
            print("done.\n")
            pass
        elif (keyboard.read_key()) == "f8":
            return True
        else:
            system(clear)
            print("Exiting")
            sleep(0.3)
            system(clear)
            print("Exiting.")
            sleep(0.3)
            system(clear)
            print("Exiting..")
            sleep(0.3)
            system(clear)
            print("Thank you for using Doppelkey, goodbye.")
            sleep(0.3)
            raise SystemExit()

    def keyplay(rep, num, speed):
        while (rep <= num):            
            keyboard.play(keyboard_recording, speed_factor=speed)
            rep += 1

    def mouseplay(rep, num, speed, pos):
        #rep = rep
        while (rep <= num):
            mouse.move(pos[0], pos[1], absolute=True, duration=0)
            mouse.play(mouse_recording, speed_factor=speed, include_wheel=True, include_clicks=True)
            rep += 1


#First run
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
    mouse_recording = []
    keyboard.wait("f8")
    pos = mouse.get_position()
    print("start")
    mouse.hook(mouse_recording.append)
    keyboard.start_recording()
    keyboard.wait("f8")
    print("stop")
    mouse.unhook(mouse_recording.append)
    keyboard_recording = keyboard.stop_recording()

    print("Press f7 to replay the recording.")
    keyboard.wait("f7")
    sleep(1)

    keyplaythread = Thread(target=lambda :keyplay(rep, num, speed))
    mouseplaythread = Thread(target=lambda :mouseplay(rep, num, speed, pos))

    keyplaythread.start()
    mouseplaythread.start()

    keyplaythread.join()
    mouseplaythread.join()
    system(clear)
    print("done\n")
    

#Rerun
    while (True):
        print("If you wish to replay the recordings again, press f7.")
        print("If you wish to start over, press f8.")
        print("Press any other key to quit the application.")
        if (replay()):
            break
