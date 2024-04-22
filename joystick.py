import ctypes
import subprocess
from sdl2 import *

# https://stackoverflow.com/questions/19691251/catching-joystick-events-with-pysdl2

REWASD_COMMAND_LINE_EXE = "C:\\Program Files\\reWASD\\reWASDCommandLine.exe"
CONTROLLER_DEVICE_ID = "113426740372824"
REWASD_CONFIG = "C:\\Users\\Public\\Documents\\reWASD\\Profiles\\Desktop\\Controller\\Config 1.rewasd"
REWASD_SLOT = 1

class Joystick:
    def __init__(self):
        SDL_SetHint(SDL_HINT_JOYSTICK_ALLOW_BACKGROUND_EVENTS, b"1")
        SDL_Init(SDL_INIT_EVERYTHING)
        self.devices = {}

    def update(self):
        event = SDL_Event()
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_JOYDEVICEADDED:
                device = SDL_JoystickOpen(event.jdevice.which)
                id = SDL_JoystickGetDeviceInstanceID(event.jdevice.which)
                self.devices[id] = device
                # print(F"joy added: {id}, {SDL_JoystickName(device)}, {SDL_JoystickGetVendor(device)}")
            elif event.type == SDL_JOYDEVICEREMOVED:
                if (id := event.jdevice.which) in self.devices:
                    SDL_JoystickClose(self.devices[id])
                    del self.devices[id]
                    # print(F"joy removed: {id}")
            elif event.type == SDL_JOYBUTTONUP:
                # print("joy button up!")
                subprocess.run([REWASD_COMMAND_LINE_EXE,
                                "apply", "--id", CONTROLLER_DEVICE_ID, "--path", REWASD_CONFIG, "--slot", F"slot{REWASD_SLOT}"])
