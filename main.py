import time
from joystick import Joystick

if __name__ == "__main__":
    joystick = Joystick()
    while True:
        joystick.update()
        time.sleep(0.1)
