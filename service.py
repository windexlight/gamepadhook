import ctypes
import subprocess
import time
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
from sdl2 import *


class Joystick:
    def __init__(self):
        SDL_Init(SDL_INIT_JOYSTICK)

    def update(self):
        event = SDL_Event()
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_JOYDEVICEADDED:
                self.device = SDL_JoystickOpen(event.jdevice.which)
                self.deviceid = SDL_JoystickGetDeviceInstanceID(event.jdevice.which)
                # print(F"joy added: {self.deviceid}")
                # print(F"num joy: {SDL_NumJoysticks()}")
            elif event.type == SDL_JOYDEVICEREMOVED:
                # print(F"joy removed: {event.jdevice.which}")
                if self.deviceid == event.jdevice.which:
                    SDL_JoystickClose(self.device)
                # print(F"num joy: {SDL_NumJoysticks()}")
            elif event.type == SDL_JOYBUTTONUP:
                # print("Button up!")
                subprocess.run(["C:\\Program Files\\reWASD\\reWASDCommandLine.exe",
                                "apply", "--id", "113426740372824", "--path", "C:\\Users\\Public\\Documents\\reWASD\\Profiles\\Desktop\\Controller\\Config 1.rewasd", "--slot", "slot1"])


class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "GamepadHook"
    _svc_display_name_ = "GamepadHook"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)
        self.run = False

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.run = False

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.run = True
        self.main()

    def main(self):
        joystick = Joystick()
        while self.run:
            joystick.update()
            time.sleep(0.1)


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)