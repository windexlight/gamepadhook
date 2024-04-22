# GamepadHook

## Description

GamepadHook is a very simple Python script that can be run in the background as a Windows service. When a button is pressed on a connected game controller, the reWASD command line interface is used to enable a config to start mapping.

## Scenario

A PC has a game controller as the only easily accessible input device. Mouse and keyboard are either not present or require extra effort to get to. The intention is the PC be fully and easily usable for all intended purposes with only the game controller. Perhaps this is a home theater PC or one used for couch gaming. Who wants to have a mouse and keyboard lying around in their living room?

reWASD has been set up to allow the controller to emulate mouse and keyboard for all desired purposes.

## Problem

In some circumstances, reWASD may return to a default state in which all mappings are turned off, and controllers are returned to native behavior. Perhaps you wake the PC from sleep, turn on the controller, and find that you have no control of the PC because reWASD mappings are inexplicably off. You then utter an expletive and have to waste your valuable downtime getting to your mouse and keyboard so you can get reWASD enabled before you can get to what you wanted to do. You then question your life choices and wonder why in the world you decided to connect a PC to your TV in the first place.

reWASD itself does not seem to provide any native means of re-enabling a config using only the controller once mappings have been turned off, nor does it provide a reliable means of having a "default" or "desktop mode" config that will always be auto-enabled when no specific application has the focus.

## Solution

A simple Python script that uses [PySDL2](https://github.com/py-sdl/py-sdl2) to monitor all connected gamepads for input. When any digital button is pressed, the reWASD command line interface is used to enable a config. While the script is running, if you find yourself in the above situation in which you lack control of the PC, just press any button on the controller and reWASD mappings will be enabled. The script can be run as a Windows service so it is always active in the background.

An analagous C/C++ program could be created to do the same thing without requiring Python. This is a quick solution and was easy to get working with minimal effort.

## Setup

For running a Python script as a service, pywin32 is used. No easy solution was found to start the service with the script in a Python virtual environment (venv), therefore all dependencies must be installed in the global Python installation.

1. Install Python. Tested with Python 3.12.3.
1. Make sure both the global python.exe and pip.exe are on the PATH.
1. Run these commands to install the necessary packages:
    ```
    pip install pysdl2 pysdl2-dll
    pip install pywin32
    python [path to Python installation]/Scripts/pywin32_postinstall.py -install
    ```
1. Open `joystick.py` from the GamepadHook source folder.
    1. Edit `REWASD_COMMAND_LINE_EXE` to the path of your `reWASDCommandLine.exe` if necessary . The default value should work for a typical reWASD installation.
    1. Edit `CONTROLLER_DEVICE_ID` to the Device ID of your controller as found in the reWASD GUI. Open your config in reWASD, right-click the icon for your controller at the bottm of the interface, and select `Copy device ID`.
    1. Edit `REWASD_CONFIG` to the path of your .rewasd config file. This will be the config enabled on your controller when you press a button.
    1. Edit `REWASD_SLOT` to the slot you want to apply the config to. If you're not using slots, then 1 should be fine.
    1. Save the file.
1. From the GamepadHook source folder, use these commands to install and then start the script as a Windows service:
    ```
    python service.py install
    python service.py start
    ```
1. To set the service to automatically start when the PC reboots, type Win+R and run `services.msc`. Find `GamepadHook` in the list of services. You should see its Status is `Running` and Startup Type is `Manual`. Right-click it and select `Properties`. Change Startup type to `Automatic`.
1. If you wish to stop the service, this can be done by right-clicking its entry in `services.msc`, or else you can use these commands in the GamepadHook source folder to stop and/or uninstall the service:
    ```
    python service.py stop
    python service.py remove
    ```
1. If you make any changes to the Python source while the service is running, you will need to restart it using the above stop and start commands or from `services.msc`.

## Notes

When testing the script for the first time, if you have the reWASD GUI open, the script will likely not detect your controller. While the reWASD GUI is open, it hooks the controller to enable pressing buttons on the controller to auto-navigate you to the button for mapping it. Close the reWASD GUI, and test by right-clicking the reWASD tray icon to disable mappings. Then press a button on your controller, and your config should be enabled.

Only button presses that trigger SDL_JOYBUTTONUP events will be caught by the script. Which physical buttons these are will likely vary from controller to controller.

If it is desired to make the native controller behavior usable with reWASD mappings turned off, the script could be edited to look for a specific combination of controller buttons being pressed to trigger reWASD enable. This does not matter to me, so I did not bother.

The script intends to catch any button press from any controller recognized by SDL2. If your reWASD config has a virtual controller enabled (with the intention that certain button presses are mapped to virtual controller button presses on the output), then the virtual controller button presses will be caught by the script. This may have unintented side effects. No easy way of deterministically identifying reWASD virtual controllers to blacklist them was found, so a brief attempt to do so was abandoned (it does not matter for my use case anyway). If it matters to you, you'll have to find a way to work around it (perhaps by editing the script to look for events exclusively from your whitelisted controller).

If you wish to test the script in isolation without starting it as a service, you can do so by running main.py. If you uncomment the `print` lines in joystick.py, you can get it to output messages to verify when controllers are connected/disconnected and when button presses are caught.

You can also adjust the polling rate by changing the value passed to `sleep` in service.py (or main.py if you're testing that way). The script is using 0.1 by default, so it is waking up about every 100ms to service SDL2 events. This doesn't lead to any significant CPU usage. If you'd like to reduce it even further, feel free to increase the value at the expense of a slower response time to button presses.

## Assumptions

- Tested only with Python 3.12.3, PySDL2 0.9.16, pysdl2-dll 2.30.2, and pywin32 306.
- Tested only on Windows 11 version 23H2.
- Tested with a single Flydigi Vader 3 Pro controller connected to the system via dongle in Dinput mode (blue LED), which seems to be the only mode that reWASD fully supports with the V3P.
- Tested with the V3P in Xinput mode also, and verified that the script correctly catches button presses (although it is not fully supported by reWASD in this mode).
- Tested briefly with a DualSense connected to the PC via Bluetooth, and verified that a DualSense button press was caught by the script.