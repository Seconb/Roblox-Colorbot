import keyboard # Library that relates to reading and writing keyboard inputs
import os
import mss # Takes screenshot
import configparser
import cv2 # Reads through screenshot
import numpy as np # Works with CV2
import win32api # Windows API that I just use for mouse button keybinds and mouse movement to an enemy
import win32con
from threading import Thread
from colorama import Fore, Style # Makes the colorful text in the console
import ctypes # Also Windows API to move the mouse
import time # Allows for specific time delays and such
import pygetwindow as gw # Only takes screenshots when youre actually playing
from urllib.request import urlopen
from webbrowser import open as openwebpage
#importing all the modules we need to run the code.
switchmodes = ("Hold", "Toggle") #this is a tuple of [0, 1] where hold is 0, toggle is 1. 

user32 = ctypes.windll.user32
kernel = np.ones((3, 3), np.uint8) # 3x3 array of 1s for structuring purposes

# its important that you change (if youre using pyinstaller) os.path.dirname(__file__) to os.path.dirname(os.path.dirname(__file__))
config_file_path = os.path.join(os.path.dirname(__file__), "config.ini") # Searching for the file called config.ini to read settings

try: # checks for updates using the version number we defined earlier, pasted from andrewdarkyy cuz im lazy and his colorbot is just a modded version of mine so like who cares
    if not "7" in urlopen("https://raw.githubusercontent.com/Seconb/Arsenal-Colorbot/main/version.txt").read().decode("utf-8"):
        print("Outdated version, redownload: https://github.com/Seconb/Arsenal-Colorbot/releases")
        while True:
            time.sleep(0.1)
except Exception as e:
    print("Error checking update: ", e)
    print("Continuing anyway!")
    time.sleep(5)
    pass

try:
    config = configparser.ConfigParser() #this is separating all the config options you set.
    config.optionxform = str
    config.read(config_file_path)
except Exception as e:
        print("Error reading config:", e)

try:
    os.system("title Colorbot")
except Exception as e:
    print("Error setting the title:", e)

def rbxfocused():
    try:
        return "Roblox" in gw.getActiveWindow().title
    except:
        return False

def change_config_setting(setting_name, new_value): #changing the config settings ... duh.
    try:
        config.set("Config", setting_name, str(new_value))
        with open(config_file_path, "w") as configfile:
            config.write(configfile)
        loadsettings()  # Update global variables after changing config
        print(f"Config setting '{setting_name}' changed to {new_value}")
    except Exception as e:
        print(f"Error changing config setting '{setting_name}': {e}")

def loadsettings(): #loading the settings, duh.
    global AIM_KEY, SWITCH_MODE_KEY, FOV_KEY_UP, FOV_KEY_DOWN, CAM_FOV, AIM_OFFSET_Y, AIM_OFFSET_X, AIM_SPEED_X, AIM_SPEED_Y, upper, lower, UPDATE_KEY, AIM_FOV, BINDMODE, COLOR, colorname, TRIGGERBOT, TRIGGERBOT_DELAY, SMOOTHENING, SMOOTH_FACTOR, TRIGGERBOT_DISTANCE
    #these are essential variables that show the settings of the application.

    try: #read the config file again, just in case if the user changed the settings while the program was running.
        config = configparser.ConfigParser() #this is separating all the config options you set.
        config.optionxform = str
        config.read(config_file_path)
    except Exception as e:
        print("Error reading config:", e)
    
    try:
        BINDMODE = config.get("Config", "BINDMODE")
        if (
            BINDMODE.lower() == "win32"
            or BINDMODE.lower() == "win32api"
            or BINDMODE.lower() == "win"
        ):
            AIM_KEY_STRING = config.get("Config", "AIM_KEY")
            if "win32con" in AIM_KEY_STRING:
                AIM_KEY = eval(AIM_KEY_STRING, {"win32con": win32con})
            else:
                AIM_KEY = str(AIM_KEY_STRING)
        if (
            BINDMODE.lower() == "keyboard"
            or BINDMODE.lower() == "k"
            or BINDMODE.lower() == "key"
        ):
            AIM_KEY = config.get("Config", "AIM_KEY")
        SWITCH_MODE_KEY = config.get("Config", "SWITCH_MODE_KEY")
        UPDATE_KEY = config.get("Config", "UPDATE_KEY")
        FOV_KEY_UP = config.get("Config", "FOV_KEY_UP")
        FOV_KEY_DOWN = config.get("Config", "FOV_KEY_DOWN")
        CAM_FOV = int(config.get("Config", "CAM_FOV"))
        AIM_FOV = int(config.get("Config", "AIM_FOV"))
        AIM_OFFSET_Y = int(config.get("Config", "AIM_OFFSET_Y"))
        AIM_OFFSET_X = int(config.get("Config", "AIM_OFFSET_X"))
        AIM_SPEED_X = float(config.get("Config", "AIM_SPEED_X"))
        AIM_SPEED_Y = float(config.get("Config", "AIM_SPEED_Y"))
        TRIGGERBOT = config.get("Config", "TRIGGERBOT")
        TRIGGERBOT_DELAY = int(config.get("Config", "TRIGGERBOT_DELAY"))
        TRIGGERBOT_DISTANCE = int(config.get("Config", "TRIGGERBOT_DISTANCE"))
        SMOOTHENING = config.get("Config", "SMOOTHENING")
        SMOOTH_FACTOR = float(config.get("Config", "SMOOTH_FACTOR"))
        if SMOOTH_FACTOR <= 0:
            SMOOTHENING = "disabled"
        COLOR = config.get("Config", "COLOR")
        if COLOR.lower() == "yellow":
            colorname = Fore.YELLOW
            upper = np.array((38, 255, 203), dtype="uint8") # The upper and lower ranges defined are the colors that the aimbot will detect and shoot at
            lower = np.array((30, 255, 201), dtype="uint8") # It's basically a group of a VERY specific shade of yellow (in this case) that it will shoot at and nothing else. The format is HSV, which differs from RGB.
        if COLOR.lower() == "blue":
            colorname = Fore.BLUE
            upper = np.array((123, 255, 217), dtype="uint8")
            lower = np.array((113, 206, 189), dtype="uint8")
        if COLOR.lower() == "pink" or COLOR.lower() == "magenta" or COLOR.lower() == "purple":
            colorname = Fore.MAGENTA
            upper = np.array((150, 255, 201), dtype="uint8")
            lower = np.array((150, 255, 200), dtype="uint8")
        if COLOR.lower() == "green":
            colorname = Fore.GREEN
            upper = np.array((60, 255, 201), dtype="uint8")
            lower = np.array((60, 255, 201), dtype="uint8")
        if COLOR.lower() == "cyan":
            colorname = Fore.CYAN
            upper = np.array((90, 255, 201), dtype="uint8")
            lower = np.array((90, 255, 201), dtype="uint8")

    except Exception as e:
        print("Error loading settings:", e)
        
try:
    loadsettings() #try to catch any errors with the settings maybe a typo or something.
except Exception as e:
    print("Error loading settings:", e)

sct = mss.mss()
screenshot = sct.monitors[1] #this is the settings for the screen capture, the program screenshots your first monitor and continues to look for enemies.
screenshot["left"] = int((screenshot["width"] / 2) - (CAM_FOV / 2))
screenshot["top"] = int((screenshot["height"] / 2) - (CAM_FOV / 2))
screenshot["width"] = CAM_FOV
screenshot["height"] = CAM_FOV
center = CAM_FOV / 2

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

def lclc():
    try:
        return win32api.GetAsyncKeyState(AIM_KEY) < 0 #checking if the aim key is pressed (mouse buttons)
    except Exception as e:
        print("Error checking key state:", e)

class trb0t:
    def __init__(self): #initialize the code, first set the variables for default settings.
        self.AIMtoggled = False
        self.switchmode = 1 # as i said earlier, the array is 0-1, 0 being hold, 1 being toggle. the default is TOGGLE as you can see.
        self.__clicks = 0 # clicks to keep track of colorbot
        self.__shooting = False

    def __stop(self):
        oldclicks = self.__clicks
        time.sleep(.05)
        if self.__clicks == oldclicks:
            user32.mouse_event(0x0004)

    def __delayedaim(self):
        self.__shooting = True
        time.sleep(TRIGGERBOT_DELAY / 1000)
        user32.mouse_event(0x0002)
        self.__clicks += 1
        Thread(target = self.__stop).start()
        self.__shooting = False

    def process(self): #process all images we're capturing
        if rbxfocused():
            try: 
                img = np.array(sct.grab(screenshot)) #grab screenshot
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #grab hsv color format
                mask = cv2.inRange(hsv, lower, upper) # create a mask of only the enemy colors
                dilated = cv2.dilate(mask, kernel, iterations=5) # dilation makes objects appear larger for the aimbot
                thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1] # threshold
                (contours, hierarchy) = cv2.findContours(
                    thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE # find contours
                )
                if len(contours) != 0: # if enemies are on screen: (or if there are contours of enemies on screen)
                    contour = max(contours, key=cv2.contourArea)
                    topmost = tuple(contour[contour[:, :, 1].argmin()][0]) #finds the highest contour vertically (highest point of the enemy, their head)
                    x = topmost[0] - center + AIM_OFFSET_X # calculating the perfect center of the enemy's head by offsetting it a set amount of pixels
                    y = topmost[1] - center + AIM_OFFSET_Y
                    distance = np.sqrt(x**2 + y**2) # basic distance in a 2d plane. calculated using pythagorean theorem.
                    if distance <= AIM_FOV:
                        x2 = x * AIM_SPEED_X
                        y2 = y * AIM_SPEED_Y
                        x2 = int(x2)
                        y2 = int(y2)
                        if SMOOTHENING.lower() != "disabled":
                            if distance >= SMOOTH_FACTOR:
                                user32.mouse_event(0x0001, x2, y2, 0, 0) #move the mouse towards, usually should feel like aimassist.
                        else:
                            user32.mouse_event(0x0001, x2, y2, 0, 0) #move the mouse towards, usually should feel like aimassist.
                        if TRIGGERBOT != "disabled" and distance <= TRIGGERBOT_DISTANCE:
                            if TRIGGERBOT_DELAY != 0:
                                if self.__shooting == False:
                                    Thread(target = self.__delayedaim).start()
                            else:
                                user32.mouse_event(0x0002)
                                self.__clicks += 1
                                Thread(target = self.__stop).start()
                        
            except Exception as e:
                print("Error in processing:", e)

    def AIMtoggle(self):
        try:
            self.AIMtoggled = not self.AIMtoggled
            time.sleep(0.1) # very short cooldown to stop it from thinking we're rapid toggling.
        except Exception as e:
            print("Error toggling AIM:", e)

    def modeswitch(self): #switch the modes from again, the array, from 0 to 1, 0 being hold, 1 being toggle.
        try:
            if self.switchmode == 0:
                self.switchmode = 1
            elif self.switchmode == 1:
                self.switchmode = 0
            time.sleep(0.1)
        except Exception as e:
            print("Error switching modes:", e)


def print_banner(b0t: trb0t): #Printing the information
    try:
        os.system("cls") # First clearing the terminal, to then re-print with the new information. Note the colorama formatting with styling and colors!
        print(
            Style.BRIGHT
            + Fore.CYAN
            + """
    _   ___  ___ ___ _  _   _   _       ___ ___  _    ___  ___ ___  ___ _____ 
   /_\ | _ \/ __| __| \| | /_\ | |     / __/ _ \| |  / _ \| _ \ _ )/ _ \_   _|
  / _ \|   /\__ \ _|| .` |/ _ \| |__  | (_| (_) | |_| (_) |   / _ \ (_) || |  
 /_/ \_\_|_\|___/___|_|\_/_/ \_\____|  \___\___/|____\___/|_|_\___/\___/ |_|                                                                                                                                                                                                                      
"""
            + Style.RESET_ALL
        )
        print("====== Controls ======")
        print("Activate colorbot    :", Fore.YELLOW + str(AIM_KEY) + Style.RESET_ALL)
        if SWITCH_MODE_KEY != "disabled":
            print("Switch toggle/hold   :", Fore.YELLOW + SWITCH_MODE_KEY + Style.RESET_ALL)
        if UPDATE_KEY != "disabled":
            print("Update Config        :", Fore.YELLOW + UPDATE_KEY + Style.RESET_ALL)
        if FOV_KEY_UP != "disabled" and FOV_KEY_DOWN != "disabled":
            print(
                "Change FOV           :",
                Fore.YELLOW + FOV_KEY_UP + "/" + FOV_KEY_DOWN + Style.RESET_ALL,
            )
        print("==== Information =====")
        print(
            "Toggle/Hold Mode     :",
            Fore.CYAN + switchmodes[b0t.switchmode] + Style.RESET_ALL,
        )
        print("Aim FOV              :", Fore.CYAN + str(AIM_FOV) + Style.RESET_ALL)
        print("Cam FOV              :", Fore.CYAN + str(CAM_FOV) + Style.RESET_ALL)
        if TRIGGERBOT != "disabled":
            print("Triggerbot           :", Fore.GREEN + "On" + Style.RESET_ALL)
        else:
            print("Triggerbot           :", Fore.RED + "Off" + Style.RESET_ALL)
        if TRIGGERBOT_DELAY != 0:
            print("Triggerbot Delay     :", Fore.GREEN + str(TRIGGERBOT_DELAY) + Style.RESET_ALL)
        if SMOOTHENING != "disabled":
            print("Smoothening          :", Fore.GREEN + "On" + Style.RESET_ALL)
            print("Smoothening Factor   :", Fore.CYAN + str(SMOOTH_FACTOR) + Style.RESET_ALL)
        else:
            print("Smoothening          :", Fore.RED + "Off" + Style.RESET_ALL)
        if TRIGGERBOT_DELAY != 0:
            print("Triggerbot Delay     :", Fore.GREEN + str(TRIGGERBOT_DELAY) + Style.RESET_ALL)
        print(
            "Aim Speed            :",
            Fore.CYAN
            + "X: "
            + str(AIM_SPEED_X)
            + " Y: "
            + str(AIM_SPEED_Y)
            + Style.RESET_ALL,
        )
        print(
            "AiM Offset           :",
            Fore.CYAN
            + "X: "
            + str(AIM_OFFSET_X)
            + " Y: "
            + str(AIM_OFFSET_Y)
            + Style.RESET_ALL,
        )
        print(
            "Aim Activated        :",
            (Fore.GREEN if b0t.AIMtoggled else Fore.RED)
            + str(b0t.AIMtoggled)
            + Style.RESET_ALL,
        )
        print(
            "Enemy Color          :",
            str(colorname + COLOR) + Style.RESET_ALL
                    )
        print("======================")
        print(
            Style.BRIGHT
            + Fore.CYAN
            + "https://discord.gg/nDREsRUj9V for configs and help!"
            + Style.RESET_ALL
        )
    except Exception as e:
        print("Error printing banner:", e)

try:
    buffer = open(os.path.join(os.path.dirname(__file__), "lastlaunch.txt"), "r")
    currenttime = time.time()
    if currenttime - float(buffer.read()) >= 17990:
        buffer2 = open(os.path.join(os.path.dirname(__file__), "lastlaunch.txt"), "w+")
        buffer2.write(str(currenttime))
        buffer2.close()
        openwebpage("https://discord.gg/nDREsRUj9V")
    buffer.close()
except:
    buffer = open(os.path.join(os.path.dirname(__file__), "lastlaunch.txt"), "w+")
    buffer.write(str(time.time()))
    buffer.close()
    openwebpage("https://discord.gg/nDREsRUj9V")

if __name__ == "__main__":
    b0t = trb0t() #the main class we made earlier
    try:
        print_banner(b0t) #to update information or print initial info.
        while True:
            # under each if statement, we first check if the key is set to disabled (if it is disabled, then it will not function. this allows the user to disable keys they don't wish to use.
            if SWITCH_MODE_KEY != "disabled" and keyboard.is_pressed(SWITCH_MODE_KEY):
                b0t.modeswitch() #switching the mode if the user presses the switch mode key AND its not disabled.
                print_banner(b0t) #updating the information
            if FOV_KEY_UP != "disabled" and keyboard.is_pressed(FOV_KEY_UP):
                change_config_setting("AIM_FOV", AIM_FOV+5) #same thing as before, just adding 5 increments to the fov.
                print_banner(b0t)
            if FOV_KEY_DOWN != "disabled" and keyboard.is_pressed(FOV_KEY_DOWN):
                change_config_setting("AIM_FOV", AIM_FOV-5) #same thing as before just removing 5 increments
                print_banner(b0t)
            if UPDATE_KEY != "disabled" and keyboard.is_pressed(UPDATE_KEY):
                loadsettings() #updating the settings if the user presses the update key.
                print_banner(b0t)
            

            time.sleep(0.1) #.1s cooldown as a way of preventing lag and mispresses

            if (
                BINDMODE.lower() == "win32"
                or BINDMODE.lower() == "win32api"
                or BINDMODE.lower() == "win" #make all strings lowercase just in case if someone in config typed it out as WIN32API, which the code wouldn't recognize.
            ): # this is mostly for the mouse buttons.
                if lclc(): #if user is holding down on the key or a key.
                    if b0t.switchmode == 0: #if mode is on [**0**, 1] (means if 0) which is hold.
                        while lclc(): #while the user is holding the key.
                            if not b0t.AIMtoggled: 
                                b0t.AIMtoggle() #and if the aim isn't already activated, activate it.
                                print_banner(b0t) #update info
                                while b0t.AIMtoggled: 
                                    b0t.process() #while it is on/activated THEN process all screen capture, note that it doesn't process information unless activated.
                                    if not lclc(): 
                                        b0t.AIMtoggle() #if user stops holding the key, it'll turn off the colorbot.
                                        print_banner(b0t) #update info.
                    if b0t.switchmode == 1: #if mode is on [0, **1**] (means if toggled)
                        b0t.AIMtoggle() # activate it forever until user presses again.
                        print_banner(b0t)
                        while b0t.AIMtoggled: #while it is toggled
                            b0t.process() # process the images.
                            if lclc():
                                b0t.AIMtoggle() # if user presses the button, then deactivate
                                print_banner(b0t) #update info
            else:
                if keyboard.is_pressed(AIM_KEY): #else if the user uses keyboard config, then look for keyboard buttons instead.
                    if b0t.switchmode == 0:
                        while keyboard.is_pressed(AIM_KEY): # SAME EXACT PROCESS AS THE MOUSE KEY PRESSES ABOVE, REFER THERE.
                            if not b0t.AIMtoggled:
                                b0t.AIMtoggle()
                                print_banner(b0t)
                                while b0t.AIMtoggled:
                                    b0t.process()
                                    if not keyboard.is_pressed(AIM_KEY):
                                        b0t.AIMtoggle()
                                        print_banner(b0t)
                    if b0t.switchmode == 1: 
                        b0t.AIMtoggle() # SAME EXACT PROCESS AS THE MOUSE KEY PRESSES ABOVE, REFER THERE.
                        print_banner(b0t)
                        while b0t.AIMtoggled:
                            b0t.process()
                            if keyboard.is_pressed(AIM_KEY):
                                b0t.AIMtoggle()
                                print_banner(b0t)
    except Exception as e:
        print("An error occurred:", e) #the end, DM befia on discord if you need clarity. Info by, duh, befia or taylor.
