import time
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
from joystick import Joystick

# https://stackoverflow.com/questions/32404/how-do-you-run-a-python-script-as-a-service-in-windows
# https://stackoverflow.com/questions/63754895/how-to-create-windows-service-using-python

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