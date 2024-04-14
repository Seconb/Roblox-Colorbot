from keyboard import is_pressed # Library that relates to reading and writing keyboard inputs
from os import system, chdir
from os.path import dirname, join
import mss # Takes screenshot
import configparser
from cv2 import dilate, threshold, findContours, RETR_EXTERNAL, CHAIN_APPROX_NONE, contourArea, cvtColor, COLOR_BGR2HSV, inRange, THRESH_BINARY # examines screenshot
import numpy as np # Works with CV2
import win32api # Windows API that I just use for mouse button keybinds and mouse movement to an enemy
from threading import Thread
from colorama import Fore, Style # Makes the colorful text in the console
from time import time, sleep, strftime, localtime # Allows for specific time delays and such
import pygetwindow as gw # Only takes screenshots when youre actually playing
from urllib.request import urlopen
from webbrowser import open as openwebpage
from math import sqrt
import sys
from keybinds import *
kernel = np.ones((3, 3), np.uint8) # 3x3 array of 1s for structuring purposes
toggleholdmodes = ("Hold", "Toggle") #this is a tuple of [0, 1] where hold is 0, toggle is 1. 
#importing all the modules we need to run the code.

def log_error(error_message):
    timestamp = strftime('%Y-%m-%d %H:%M:%S', localtime())
    log_entry = f"{timestamp}: {error_message}\n"
    try:
        with open(error_log_path, 'a') as log_file:
            log_file.write(log_entry)
    except FileNotFoundError:
        with open(error_log_path, 'w') as log_file:
            log_file.write(log_entry)

try: # if the user is running the exe, find the config and time they last opened the file relative to the exe, else do it relative to the .py file.
    if getattr(sys, 'frozen', False):
        application_path = dirname(sys.executable)
        config_file_path = join(application_path, 'config.txt')
        last_launch_path = join(application_path, 'lastlaunch.txt')
        error_log_path = join(application_path, "log.txt")
        chdir(application_path)
    else:
        script_directory = dirname(__file__)
        config_file_path = join(script_directory, "config.txt")
        last_launch_path = join(script_directory, "lastlaunch.txt")
        error_log_path = join(script_directory, "log.txt")
        chdir(script_directory)
except Exception as e:
    print(f"An error occurred checking if you're using the .py or the .exe: {e}")
    log_error(e)
    exit()

try:
    buffer = open(last_launch_path, "r")
    currenttime = time()
    if currenttime - float(buffer.read()) >= 17990:
        buffer2 = open(last_launch_path, "w+")
        buffer2.write(str(currenttime))
        buffer2.close()
        openwebpage("https://discord.gg/thunderclient")
        buffer.close()
except:
    buffer = open(last_launch_path, "w+")
    buffer.write(str(currenttime))
    buffer.close()
    openwebpage("https://discord.gg/thunderclient")

try: # checks for updates using the version number we defined earlier, pasted from andrewdarkyy cuz im lazy and his colorbot is just a modded version of mine so like who cares
    if not "11" in urlopen("https://raw.githubusercontent.com/Seconb/Arsenal-Colorbot/main/version.txt").read().decode("utf-8"):
        print("Outdated version, redownload: https://github.com/Seconb/Arsenal-Colorbot/releases")
        while True:
            sleep(0.1)
except Exception as e:
    print("Error checking update: ", e)
    log_error(e)
    print("Continuing anyway!")
    sleep(5)
    pass

try:
    config = configparser.ConfigParser() #this is separating all the config options you set.
    config.optionxform = str
    config.read(config_file_path)
except Exception as e:
        print("Error reading config:", e)
        log_error(e)
        exit()

def rbxfocused():
    try:
        return "Roblox" == gw.getActiveWindow().title
    except AttributeError:
        # if youre in the middle of alt tabbing it screws things up, so we'll just ignore if youre doing that
        return False
    except Exception as e:
        print("An error occurred checking if Roblox is focused: ", e)
        log_error(e)
        exit()

def change_config_setting(setting_name, new_value): #changing the config settings ... duh.
    try:
        config.set("Config", setting_name, str(new_value))
        with open(config_file_path, "w") as configfile:
            config.write(configfile)
        load()  # Update global variables after changing config
        print(f"Config setting '{setting_name}' changed to {new_value}")
    except Exception as e:
        print(f"Error changing config setting '{setting_name}': {e}")
        log_error(e)
        exit()

def load(): #loading the settings, duh.
    global sct, center, screenshot, AIM_KEY, SWITCH_MODE_KEY, FOV_KEY_UP, FOV_KEY_DOWN, CAM_FOV, AIM_OFFSET_Y, AIM_OFFSET_X, AIM_SPEED_X, AIM_SPEED_Y, upper, lower, UPDATE_KEY, AIM_FOV, BINDMODE, COLOR, colorname, TRIGGERBOT, TRIGGERBOT_DELAY, SMOOTHENING, SMOOTH_FACTOR, TRIGGERBOT_DISTANCE
    #these are essential variables that show the settings of the application.
    system("title Colorbot")
    
    try: #read the config file again, just in case if the user changed the settings while the program was running.
        config = configparser.ConfigParser() #this is separating all the config options you set.
        config.optionxform = str
        config.read(config_file_path)
    except Exception as e:
        print("Error reading config:", e)
        log_error(e)
        exit()

    try:
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
        UPPER_COLOR = tuple(map(int, config.get("Config", "UPPER_COLOR").split(', '))) # pasted from the modded colorbot but we're partnered so its chill
        LOWER_COLOR = tuple(map(int, config.get("Config", "LOWER_COLOR").split(', ')))
        if SMOOTH_FACTOR <= 0:
            SMOOTHENING = "disabled"
        COLOR = config.get("Config", "COLOR")
        if COLOR.lower() == "yellow":
            colorname = Fore.YELLOW
            upper = np.array((30, 255, 229), dtype="uint8") # The upper and lower ranges defined are the colors that the aimbot will detect and shoot at
            lower = np.array((30, 255, 229), dtype="uint8") # It's basically a group of a VERY specific shade of yellow (in this case) that it will shoot at and nothing else. The format is HSV, which differs from RGB.
        if COLOR.lower() == "blue":
            colorname = Fore.BLUE
            upper = np.array((120, 255, 229), dtype="uint8")
            lower = np.array((120, 255, 229), dtype="uint8")
        if COLOR.lower() == "pink" or COLOR.lower() == "magenta" or COLOR.lower() == "purple":
            colorname = Fore.MAGENTA
            upper = np.array((150, 255, 229), dtype="uint8")
            lower = np.array((150, 255, 229), dtype="uint8")
        if COLOR.lower() == "green":
            colorname = Fore.GREEN
            upper = np.array((60, 255, 229), dtype="uint8")
            lower = np.array((60, 255, 229), dtype="uint8")
        if COLOR.lower() == "cyan":
            colorname = Fore.CYAN
            upper = np.array((90, 255, 229), dtype="uint8")
            lower = np.array((90, 255, 229), dtype="uint8")
        if COLOR.lower() == "red":
            colorname = Fore.RED
            upper = np.array((0, 255, 229), dtype="uint8")
            lower = np.array((0, 255, 229), dtype="uint8")
        if COLOR.lower() == "custom":
            colorname = Fore.WHITE
            upper = np.array(UPPER_COLOR, dtype="uint8")
            lower = np.array(LOWER_COLOR, dtype="uint8")
        if COLOR.lower() == "0000ff":
            colorname = Fore.BLUE
            upper = np.array((123, 255, 255), dtype="uint8")
            lower = np.array((120, 147, 69), dtype="uint8")
        if COLOR.lower() == "aimblox":
            colorname = Fore.LIGHTRED_EX
            upper = np.array((4, 225, 206), dtype="uint8")
            lower = np.array((0, 175, 119), dtype="uint8")
        if COLOR.lower() == "black":
            colorname = Fore.WHITE
            upper = np.array((0, 0, 0), dtype="uint8")
            lower = np.array((0, 0, 0), dtype="uint8")
        sct = mss.mss()
        screenshot = sct.monitors[1] #this is the settings for the screen capture, the program screenshots your first monitor and continues to look for enemies.
        screenshot["left"] = int((screenshot["width"] / 2) - (CAM_FOV / 2))
        screenshot["top"] = int((screenshot["height"] / 2) - (CAM_FOV / 2))
        screenshot["width"] = CAM_FOV
        screenshot["height"] = CAM_FOV
        center = CAM_FOV / 2

    except Exception as e:
        print("Error loading settings:", e)
        log_error(e)
        exit()
load()

def lclc():
    try:
        return win32api.GetAsyncKeyState(get_keycode(AIM_KEY)) < 0 #checking if the aim key is pressed
    except Exception as e:
        print("Error checking key state:", e)
        log_error(e)
        exit()

class trb0t:
    def __init__(self): #initialize the code, first set the variables for default settings.
        self.AIMtoggled = False
        self.switchmode = 1 # as i said earlier, the array is 0-1, 0 being hold, 1 being toggle. the default is TOGGLE as you can see.
        self.__clicks = 0 # clicks to keep track of colorbot
        self.__shooting = False

    def __stop(self):
        oldclicks = self.__clicks
        sleep(.05)
        if self.__clicks == oldclicks:
            win32api.mouse_event(0x0004, 0, 0, 0, 0)

    def __delayedaim(self):
        self.__shooting = True
        sleep(TRIGGERBOT_DELAY / 1000)
        win32api.mouse_event(0x0002, 0, 0, 0, 0)
        self.__clicks += 1
        Thread(target = self.__stop).start()
        self.__shooting = False

    def process(self): #process all images we're capturing
        if rbxfocused():
            try: 
                img = np.array(sct.grab(screenshot)) #grab screenshot
                hsv = cvtColor(img, COLOR_BGR2HSV) #grab hsv color format
                mask = inRange(hsv, lower, upper) # create a mask of only the enemy colors
                dilated = dilate(mask, kernel, iterations=5) # dilation makes objects appear larger for the aimbot
                thresh = threshold(dilated, 60, 255, THRESH_BINARY)[1] # threshold
                (contours, hierarchy) = findContours(thresh, RETR_EXTERNAL, CHAIN_APPROX_NONE) # finds the contours
                if len(contours) != 0: # if enemies are on screen: (or if there are contours of enemies on screen)
                    contour = max(contours, key=contourArea)
                    topmost = tuple(contour[contour[:, :, 1].argmin()][0]) #finds the highest contour vertically (highest point of the enemy, their head)
                    x = topmost[0] - center + AIM_OFFSET_X # calculating the perfect center of the enemy's head by offsetting it a set amount of pixels
                    y = topmost[1] - center + AIM_OFFSET_Y
                    distance = sqrt(x**2 + y**2) # basic distance in a 2d plane. calculated using pythagorean theorem.
                    if distance <= AIM_FOV:
                        x2 = x * AIM_SPEED_X
                        y2 = y * AIM_SPEED_Y
                        x2 = int(x2)
                        y2 = int(y2)
                        if SMOOTHENING.lower() != "disabled":
                            if distance >= SMOOTH_FACTOR:
                                win32api.mouse_event(0x0001, x2, y2, 0, 0) #move the mouse towards, usually should feel like aimassist.
                        else:
                            win32api.mouse_event(0x0001, x2, y2, 0, 0) #move the mouse towards, usually should feel like aimassist.
                        if TRIGGERBOT != "disabled" and distance <= TRIGGERBOT_DISTANCE:
                            if TRIGGERBOT_DELAY != 0:
                                if self.__shooting == False:
                                    Thread(target = self.__delayedaim).start()
                            else:
                                win32api.mouse_event(0x0002, 0, 0, 0, 0)
                                self.__clicks += 1
                                Thread(target = self.__stop).start()
                        
            except Exception as e:
                print("Error in processing:", e)
                log_error(e)
                exit()

    def AIMtoggle(self):
        try:
            self.AIMtoggled = not self.AIMtoggled
            sleep(0.15) # very short cooldown to stop it from thinking we're rapid toggling.
        except Exception as e:
            print("Error toggling aim:", e)
            log_error(e)
            exit()

    def modeswitch(self): #switch the modes from again, the array, from 0 to 1, 0 being hold, 1 being toggle.
        try:
            self.switchmode = 1 - self.switchmode
            sleep(0.15)
        except Exception as e:
            print("Error switching modes:", e)
            log_error(e)
            exit()


def print_banner(b0t: trb0t):  # Printing the information
    try:
        system("cls")  # First clearing the terminal, to then re-print with the new information. Note the colorama formatting with styling and colors!
        print(
            f"{Style.BRIGHT}{Fore.CYAN}\n"
            f"    _   ___  ___ ___ _  _   _   _       ___ ___  _    ___  ___ ___  ___ _____\n"
            f"   /_\ | _ \/ __| __| \| | /_\ | |     / __/ _ \| |  / _ \| _ \ _ )/ _ \_   _|\n"
            f"  / _ \|   /\__ \ _|| .` |/ _ \| |__  | (_| (_) | |_| (_) |   / _ \ (_) || |  \n"
            f" /_/ \_\_|_\|___/___|_|\_/_/ \_\____|  \___\___/|____\___/|_|_\___/\___/ |_|\n"
            f"{Style.RESET_ALL}"
        )
        print("====== Controls ======")
        print(f"Activate colorbot    : {Fore.YELLOW}{AIM_KEY}{Style.RESET_ALL}")
        if SWITCH_MODE_KEY != "disabled":
            print(f"Switch toggle/hold   : {Fore.YELLOW}{SWITCH_MODE_KEY}{Style.RESET_ALL}")
        if UPDATE_KEY != "disabled":
            print(f"Update Config        : {Fore.YELLOW}{UPDATE_KEY}{Style.RESET_ALL}")
        if FOV_KEY_UP != "disabled" and FOV_KEY_DOWN != "disabled":
            print(f"Change FOV           : {Fore.YELLOW}{FOV_KEY_UP}/{FOV_KEY_DOWN}{Style.RESET_ALL}")
        print("==== Information =====")
        print(f"Toggle/Hold Mode     : {Fore.CYAN}{toggleholdmodes[b0t.switchmode]}{Style.RESET_ALL}")
        print(f"Aim FOV              : {Fore.CYAN}{AIM_FOV}{Style.RESET_ALL}")
        print(f"Cam FOV              : {Fore.CYAN}{CAM_FOV}{Style.RESET_ALL}")
        if TRIGGERBOT != "disabled":
            print(f"Triggerbot           : {Fore.GREEN}On{Style.RESET_ALL}")
        else:
            print(f"Triggerbot           : {Fore.RED}Off{Style.RESET_ALL}")
        if TRIGGERBOT_DELAY != 0:
            print(f"Triggerbot Delay     : {Fore.GREEN}{TRIGGERBOT_DELAY}{Style.RESET_ALL}")
        if SMOOTHENING != "disabled":
            print(f"Smoothening          : {Fore.GREEN}On{Style.RESET_ALL}")
            print(f"Smoothening Factor   : {Fore.CYAN}{SMOOTH_FACTOR}{Style.RESET_ALL}")
        else:
            print(f"Smoothening          : {Fore.RED}Off{Style.RESET_ALL}")
        if TRIGGERBOT_DELAY != 0:
            print(f"Triggerbot Delay     : {Fore.GREEN}{TRIGGERBOT_DELAY}{Style.RESET_ALL}")
        print(
            f"Aim Speed            : {Fore.CYAN}X: {AIM_SPEED_X} Y: {AIM_SPEED_Y}{Style.RESET_ALL}"
        )
        print(
            f"Aim Offset           : {Fore.CYAN}X: {AIM_OFFSET_X} Y: {AIM_OFFSET_Y}{Style.RESET_ALL}"
        )
        print(
            f"Aim Activated        : {(Fore.GREEN if b0t.AIMtoggled else Fore.RED)}{b0t.AIMtoggled}{Style.RESET_ALL}"
        )
        print(f"Enemy Color          : {str(colorname + COLOR)}{Style.RESET_ALL}")
        print("======================")
        print(
            f"{Style.BRIGHT}{Fore.CYAN}"
            "https://discord.gg/thunderclient for configs and help!\n"
            "If you didn't download this from https://github.com/Seconb/Roblox-Colorbot, it's not legit!"
            f"{Style.RESET_ALL}"
        )
    except Exception as e:
        print("Error printing banner:", e)
        log_error(e)
        exit()


if __name__ == "__main__":
    b0t = trb0t()
    try:
        print_banner(b0t) #to update information or print initial info.
        while True:
            # under each if statement, we first check if the key is set to disabled (if it is disabled, then it will not function. this allows the user to disable keys they don't wish to use.
            if SWITCH_MODE_KEY != "disabled" and is_pressed(SWITCH_MODE_KEY):
                b0t.modeswitch() #switching the mode if the user presses the switch mode key AND its not disabled.
                print_banner(b0t) #updating the information
            if FOV_KEY_UP != "disabled" and is_pressed(FOV_KEY_UP):
                change_config_setting("AIM_FOV", AIM_FOV+5) #same thing as before, just adding 5 increments to the fov.
                print_banner(b0t)
            if FOV_KEY_DOWN != "disabled" and is_pressed(FOV_KEY_DOWN):
                change_config_setting("AIM_FOV", AIM_FOV-5) #same thing as before just removing 5 increments
                print_banner(b0t)
            if UPDATE_KEY != "disabled" and is_pressed(UPDATE_KEY):
                load() #updating the settings if the user presses the update key.
                print_banner(b0t)

            if lclc():  # If user is holding down on the key or a key.
                if b0t.switchmode == 0 and not b0t.AIMtoggled:  # If mode is on [0, 1] (means if 0) which is hold.
                    b0t.AIMtoggle()  # If the aim isn't already activated, activate it.
                    print_banner(b0t)  # Update info.
                    while lclc() and b0t.AIMtoggled:  # While the user is holding the key and aim is toggled.
                        b0t.process()  # Process screen capture.
                    if not lclc():  # If user stops holding the key.
                        b0t.AIMtoggle()  # Turn off the colorbot.
                        print_banner(b0t)  # Update info.
                elif b0t.switchmode == 1:  # If mode is on [0, 1] (means if toggled).
                    b0t.AIMtoggle()  # Activate it forever until user presses again.
                    print_banner(b0t)  # Update info.
                    while b0t.AIMtoggled:  # While it is toggled.
                        b0t.process()  # Process the images.
                        if lclc():  # If user presses the button.
                            b0t.AIMtoggle()  # Deactivate.
                            print_banner(b0t)  # Update info.
            sleep(0.03) # stops lag
    except Exception as e:
        print("An error occurred:", e) #the end, DM befia on discord if you need clarity. Info by, duh, befia or taylor.
        log_error(e)
        exit()
