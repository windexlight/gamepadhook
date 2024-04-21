import ctypes
import subprocess
import time
from sdl2 import *


class Joystick:
    def __init__(self):
        SDL_Init(SDL_INIT_JOYSTICK)# | SDL_INIT_GAMECONTROLLER)
        # SDL_SetHint(SDL_HINT_JOYSTICK_ALLOW_BACKGROUND_EVENTS, )
        # self.axis = {}
        # self.button = {}
        # SDL_JoystickOpen(0)
        # SDL_GameControllerOpen(0)
        # SDL_JoystickEventState(SDL_ENABLE)
        # print(F"num joy: {SDL_NumJoysticks()}")

    def update(self):
        event = SDL_Event()
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_JOYDEVICEADDED:
                self.device = SDL_JoystickOpen(event.jdevice.which)
                self.deviceid = SDL_JoystickGetDeviceInstanceID(event.jdevice.which)
                print(F"joy added: {self.deviceid}")
                print(F"num joy: {SDL_NumJoysticks()}")
                # SDL_JoystickEventState(SDL_ENABLE)
            # elif event.type == SDL_CONTROLLERDEVICEADDED:
            #     print(F"controller added: {event.cdevice.which}")
            #     self.device = SDL_GameControllerOpen(event.cdevice.which)
            elif event.type == SDL_JOYDEVICEREMOVED:
                print(F"joy removed: {event.jdevice.which}")
                if self.deviceid == event.jdevice.which:
                    SDL_JoystickClose(self.device)
                print(F"num joy: {SDL_NumJoysticks()}")
            # elif event.type == SDL_JOYAXISMOTION:
            #     self.axis[event.jaxis.axis] = event.jaxis.value
            # elif event.type == SDL_JOYBUTTONDOWN:
            #     print("Button down!")
            #     subprocess.run(["C:\\Program Files\\reWASD\\reWASDCommandLine.exe",
            #                     "apply", "--id", "113426740372824", "--path", "C:\\Users\\Public\\Documents\\reWASD\\Profiles\\Desktop\\Controller\\Config 1.rewasd", "--slot", "slot1"])
            #     # self.button[event.jbutton.button] = True
            elif event.type == SDL_JOYBUTTONUP:
                print("Button up!")
                subprocess.run(["C:\\Program Files\\reWASD\\reWASDCommandLine.exe",
                                "apply", "--id", "113426740372824", "--path", "C:\\Users\\Public\\Documents\\reWASD\\Profiles\\Desktop\\Controller\\Config 1.rewasd", "--slot", "slot1"])
            #     self.button[event.jbutton.button] = False


if __name__ == "__main__":
    joystick = Joystick()
    while True:
        joystick.update()
        time.sleep(0.1)
    #     # print(joystick.axis)
    #     print(joystick.button)