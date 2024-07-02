from keyboard import is_pressed
from os import system, chdir
from os.path import dirname, join
import configparser
from cv2 import dilate, threshold, findContours, RETR_EXTERNAL, CHAIN_APPROX_NONE, contourArea, cvtColor, COLOR_BGR2HSV, inRange, THRESH_BINARY
import numpy as np
import win32api
from threading import Thread
from colorama import Fore, Style
from time import time, sleep, strftime, localtime
import pygetwindow as gw
from urllib.request import urlopen
from webbrowser import open as openwebpage
from math import sqrt
import sys
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
from keybinds import *

system("title Colorbot")
kernel = np.ones((3, 3), np.uint8)
toggleholdmodes = ("Hold", "Toggle")

def log_error(error_message):
    timestamp = strftime('%Y-%m-%d %H:%M:%S', localtime())
    log_entry = f"{timestamp}: {error_message}\n"
    try:
        with open(error_log_path, 'a') as log_file:
            log_file.write(log_entry)
    except FileNotFoundError:
        with open(error_log_path, 'w') as log_file:
            log_file.write(log_entry)

try:
    if getattr(sys, 'frozen', False):
        application_path = dirname(sys.executable)
        config_file_path = join(application_path, 'config.txt')
        #last_launch_path = join(application_path, 'lastlaunch.txt')
        error_log_path = join(application_path, "log.txt")
        chdir(application_path)
    else:
        script_directory = dirname(__file__)
        config_file_path = join(script_directory, "config.txt")
        #last_launch_path = join(script_directory, "lastlaunch.txt")
        error_log_path = join(script_directory, "log.txt")
        chdir(script_directory)
except Exception as e:
    print(f"An error occurred checking if you're using the .py or the .exe: {e}")
    log_error(e)
    exit()

''' Disabled auto-joining the Discord and instead I just put the invite in the banner.
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
'''

try: # checks for updates using the version number we defined earlier, pasted from andrewdarkyy cuz im lazy and his colorbot is just a modded version of mine so like who cares
    if not "14" in urlopen("https://raw.githubusercontent.com/Seconb/Roblox-Colorbot/main/version.txt").read().decode("utf-8"):
        print("Outdated version, redownload: https://github.com/Seconb/Roblox-Colorbot/releases")
        print("Press Enter to continue anyway...")
        while True:
            if is_pressed("Enter"):
                break
except Exception as e:
    print("Error checking update: ", e)
    log_error(e)
    print("Continuing anyway!")
    sleep(5)
    pass

try:
    config = configparser.ConfigParser()
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

def change_config_setting(setting_name, new_value):
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

def load():
    global center, screenshot, camera, region, TOGGLE_HOLD_MODE, CAM_TYPE, sct, CAM_FOV_COLOR, AIM_FOV_COLOR, SHOW_FOV, AIM_KEY, SWITCH_MODE_KEY, FOV_KEY_UP, FOV_KEY_DOWN, CAM_FOV, AIM_OFFSET_Y, AIM_OFFSET_X, AIM_SPEED_X, AIM_SPEED_Y, upper, lower, UPDATE_KEY, AIM_FOV, BINDMODE, COLOR, colorname, TRIGGERBOT, TRIGGERBOT_DELAY, SMOOTHENING, SMOOTH_FACTOR, TRIGGERBOT_DISTANCE, HIDE_CONSOLE
    
    try:
        config = configparser.ConfigParser()
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
        UPPER_COLOR = tuple(map(int, config.get("Config", "UPPER_COLOR").split(', ')))
        LOWER_COLOR = tuple(map(int, config.get("Config", "LOWER_COLOR").split(', ')))
        CAM_FOV_COLOR = tuple(map(int, config.get("Config", "CAM_FOV_COLOR").split(', ')))
        AIM_FOV_COLOR = tuple(map(int, config.get("Config", "AIM_FOV_COLOR").split(', ')))
        HIDE_CONSOLE = config.get("Config", "HIDE_CONSOLE")
        SHOW_FOV = config.get("Config", "SHOW_FOV")
        CAM_TYPE = config.get("Config", "CAM_TYPE")
        TOGGLE_HOLD_MODE = config.get("Config", "TOGGLE_HOLD_MODE")
        center = CAM_FOV / 2
        if TOGGLE_HOLD_MODE.lower() == "hold":
            TOGGLE_HOLD_MODE = 0
        else:
            TOGGLE_HOLD_MODE = 1
        if CAM_TYPE.lower() == "mss":
            import mss
            sct = mss.mss()
            screenshot = sct.monitors[1] #this is the settings for the screen capture, the program screenshots your first monitor and continues to look for enemies.
            screenshot["left"] = int((screenshot["width"] / 2) - (CAM_FOV / 2))
            screenshot["top"] = int((screenshot["height"] / 2) - (CAM_FOV / 2))
            screenshot["width"] = CAM_FOV
            screenshot["height"] = CAM_FOV
        else:
            import bettercam
            usersize = [win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)]
            left, top = (usersize[0] - CAM_FOV) // 2, (usersize[1] - CAM_FOV) // 2
            right, bottom = left + CAM_FOV, top + CAM_FOV
            region = (left, top, right, bottom)
            camera = bettercam.create(output_idx=0, output_color="BGR")
        if HIDE_CONSOLE.lower() == "enabled":
            import ctypes
            import win32gui
            whnd = ctypes.windll.kernel32.GetConsoleWindow()
            if whnd != 0:
                ctypes.windll.user32.ShowWindow(whnd, 0)
                win32gui.ShowWindow(whnd, 0)
        if SMOOTH_FACTOR <= 0:
            SMOOTHENING = "disabled"
        COLOR = config.get("Config", "COLOR")
        COLORS = {
            "yellow": (Fore.YELLOW, np.array((30, 255, 229), dtype="uint8"), np.array((30, 255, 229), dtype="uint8")),
            "blue": (Fore.BLUE, np.array((120, 255, 229), dtype="uint8"), np.array((120, 255, 229), dtype="uint8")),
            "pink": (Fore.MAGENTA, np.array((150, 255, 229), dtype="uint8"), np.array((150, 255, 229), dtype="uint8")),
            "magenta": (Fore.MAGENTA, np.array((150, 255, 229), dtype="uint8"), np.array((150, 255, 229), dtype="uint8")),
            "purple": (Fore.MAGENTA, np.array((150, 255, 229), dtype="uint8"), np.array((150, 255, 229), dtype="uint8")),
            "green": (Fore.GREEN, np.array((60, 255, 229), dtype="uint8"), np.array((60, 255, 229), dtype="uint8")),
            "cyan": (Fore.CYAN, np.array((90, 255, 229), dtype="uint8"), np.array((90, 255, 229), dtype="uint8")),
            "red": (Fore.RED, np.array((0, 255, 229), dtype="uint8"), np.array((0, 255, 229), dtype="uint8")),
            "custom": (Fore.WHITE, np.array(UPPER_COLOR, dtype="uint8"), np.array(LOWER_COLOR, dtype="uint8")),
            "0000ff": (Fore.BLUE, np.array((123, 255, 255), dtype="uint8"), np.array((120, 147, 69), dtype="uint8")),
            "aimblox": (Fore.LIGHTRED_EX, np.array((4, 225, 206), dtype="uint8"), np.array((0, 175, 119), dtype="uint8")),
            "black": (Fore.WHITE, np.array((0, 0, 0), dtype="uint8"), np.array((0, 0, 0), dtype="uint8")),
        }
        try:
            colorname, upper, lower = COLORS[COLOR.lower()]
        except KeyError:
            print(f"Color '{COLOR}' is not supported.")

    except Exception as e:
        print("Error loading settings:", e)
        log_error(e)
        exit()
load()

def clicked(KEY):
    try:
        return win32api.GetAsyncKeyState(get_keycode(KEY)) < 0
    except Exception as e:
        print("Error checking key state:", e)
        log_error(e)
        exit()

def create_circle_outline_image(radius, color, alpha, outline_width):
    image = Image.new('RGBA', (2*radius, 2*radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((outline_width//2, outline_width//2, 2*radius-outline_width//2, 2*radius-outline_width//2), fill=(0, 0, 0, 0), outline=color+(alpha,), width=outline_width)
    return image

def create_circle(radius, color, alpha):
    global overlay_window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    circle_alpha = alpha  # Transparency level (0-255)
    circle_outline_width = 2  # Width of the circle outline
    circle_outline_image = create_circle_outline_image(radius, color, circle_alpha, circle_outline_width)

    circle_outline_photo = ImageTk.PhotoImage(circle_outline_image)

    overlay_window = tk.Toplevel(root)
    overlay_window.overrideredirect(True)  # Remove window decorations
    overlay_window.attributes('-topmost', True)  # Always on top
    overlay_window.attributes('-transparentcolor', 'black')  # Make the background transparent
    overlay_window.geometry(f'+{screen_width//2-radius}+{screen_height//2-radius}')  # Center the window

    circle_outline_label = tk.Label(overlay_window, image=circle_outline_photo, bg='black')
    circle_outline_label.image = circle_outline_photo  # Keep a reference to prevent garbage collection
    circle_outline_label.pack()

class trbot:
    def __init__(self):
        self.aimtoggled = False
        self.switchmode = TOGGLE_HOLD_MODE
        self.__clicks = 0
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

    def process(self):
        if rbxfocused():
            try: 
                if CAM_TYPE.lower() == "bettercam":
                    img = camera.grab(region=region)
                else:
                    img = np.array(sct.grab(screenshot))
                if img is not None:
                    hsv = cvtColor(img, COLOR_BGR2HSV)
                    mask = inRange(hsv, lower, upper)
                    dilated = dilate(mask, kernel, iterations=5)
                    thresh = threshold(dilated, 60, 255, THRESH_BINARY)[1]
                    (contours, hierarchy) = findContours(thresh, RETR_EXTERNAL, CHAIN_APPROX_NONE)
                    if len(contours) != 0:
                        contour = max(contours, key=contourArea)
                        topmost = tuple(contour[contour[:, :, 1].argmin()][0])
                        x = topmost[0] - center + AIM_OFFSET_X
                        y = topmost[1] - center + AIM_OFFSET_Y
                        distance = sqrt(x**2 + y**2)
                        if distance <= AIM_FOV:
                            x2 = x * AIM_SPEED_X
                            y2 = y * AIM_SPEED_Y
                            x2 = int(x2)
                            y2 = int(y2)
                            if SMOOTHENING.lower() != "disabled":
                                if distance >= SMOOTH_FACTOR:
                                    win32api.mouse_event(0x0001, x2, y2, 0, 0)
                            else:
                                win32api.mouse_event(0x0001, x2, y2, 0, 0)
                            if TRIGGERBOT != "disabled" and distance <= TRIGGERBOT_DISTANCE:
                                if TRIGGERBOT_DELAY != 0:
                                    if self.__shooting == False:
                                        Thread(target = self.__delayedaim).start()
                                else:
                                    win32api.mouse_event(0x0002, 0, 0, 0, 0)
                                    self.__clicks += 1
                                    Thread(target = self.__stop).start()
                else:
                    pass
                        
            except Exception as e:
                print("Error in processing:", e)
                log_error(e)
                exit()

    def aimtoggle(self):
        try:
            self.aimtoggled = not self.aimtoggled
            sleep(0.15) # very short cooldown to stop it from thinking we're rapid toggling.
        except Exception as e:
            print("Error toggling aim:", e)
            log_error(e)
            exit()

    def modeswitch(self):
        try:
            self.switchmode = 1 - self.switchmode
            sleep(0.15)
        except Exception as e:
            print("Error switching modes:", e)
            log_error(e)
            exit()
    
    def togglebot(self):
        while True:
            if clicked(AIM_KEY):
                if self.switchmode == 0 and not self.aimtoggled:
                    self.aimtoggle()
                    print_banner(self)
                    while clicked(AIM_KEY) and self.aimtoggled:
                        self.process()
                    if not clicked(AIM_KEY):
                        self.aimtoggle()
                        print_banner(self)
                elif self.switchmode == 1:
                    self.aimtoggle()
                    print_banner(self)
                    while self.aimtoggled:
                        self.process()
                        if clicked(AIM_KEY):
                            self.aimtoggle()
                            print_banner(self)
            sleep(0.01)

def print_banner(bot: trbot):
    try:
        system("cls") 
        """ # OLD LOGO
        print(
            f"{Style.BRIGHT}{Fore.CYAN}\n"
            f"    _   ___  ___ ___ _  _   _   _       ___ ___  _    ___  ___ ___  ___ _____\n"
            f"   /_\ | _ \/ __| __| \| | /_\ | |     / __/ _ \| |  / _ \| _ \ _ )/ _ \_   _|\n"
            f"  / _ \|   /\__ \ _|| .` |/ _ \| |__  | (_| (_) | |_| (_) |   / _ \ (_) || |  \n"
            f" /_/ \_\_|_\|___/___|_|\_/_/ \_\____|  \___\___/|____\___/|_|_\___/\___/ |_|\n"
            f"{Style.RESET_ALL}"                                                                        
        )
        """
        print(Style.BRIGHT + Fore.CYAN + """     
     ▄▄·       ▄▄▌        ▄▄▄  ▄▄▄▄·       ▄▄▄▄▄
    ▐█ ▌▪▪     ██•  ▪     ▀▄ █·▐█ ▀█▪▪     •██  
    ██ ▄▄ ▄█▀▄ ██▪   ▄█▀▄ ▐▀▀▄ ▐█▀▀█▄ ▄█▀▄  ▐█.▪
    ▐███▌▐█▌.▐▌▐█▌▐▌▐█▌.▐▌▐█•█▌██▄▪▐█▐█▌.▐▌ ▐█▌·
    ·▀▀▀  ▀█▄▀▪.▀▀▀  ▀█▄▀▪.▀  ▀·▀▀▀▀  ▀█▄▀▪ ▀▀▀    
        """ + Style.RESET_ALL)
        
        print("        ====== Controls ======")
        print(f"        Activate colorbot    : {Fore.YELLOW}{AIM_KEY}{Style.RESET_ALL}")
        if SWITCH_MODE_KEY != "disabled":
            print(f"        Switch toggle/hold   : {Fore.YELLOW}{SWITCH_MODE_KEY}{Style.RESET_ALL}")
        if UPDATE_KEY != "disabled":
            print(f"        Update Config        : {Fore.YELLOW}{UPDATE_KEY}{Style.RESET_ALL}")
        if FOV_KEY_UP != "disabled" and FOV_KEY_DOWN != "disabled":
            print(f"        Change FOV           : {Fore.YELLOW}{FOV_KEY_UP}/{FOV_KEY_DOWN}{Style.RESET_ALL}")
        print("        ==== Information =====")
        print(f"        Toggle/Hold Mode     : {Fore.CYAN}{toggleholdmodes[bot.switchmode]}{Style.RESET_ALL}")
        print(f"        Aim FOV              : {Fore.CYAN}{AIM_FOV}{Style.RESET_ALL}")
        print(f"        Cam FOV              : {Fore.CYAN}{CAM_FOV}{Style.RESET_ALL}")
        if TRIGGERBOT.lower() != "disabled":
            print(f"        Triggerbot           : {Fore.GREEN}On{Style.RESET_ALL}")
        else:
            print(f"        Triggerbot           : {Fore.RED}Off{Style.RESET_ALL}")
        if TRIGGERBOT_DELAY != 0:
            print(f"        Triggerbot Delay     : {Fore.GREEN}{TRIGGERBOT_DELAY}{Style.RESET_ALL}")
        if SMOOTHENING != "disabled":
            print(f"        Smoothening          : {Fore.GREEN}On{Style.RESET_ALL}")
            print(f"        Smoothening Factor   : {Fore.CYAN}{SMOOTH_FACTOR}{Style.RESET_ALL}")
        else:
            print(f"        Smoothening          : {Fore.RED}Off{Style.RESET_ALL}")
        if TRIGGERBOT_DELAY != 0:
            print(f"        Triggerbot Delay     : {Fore.GREEN}{TRIGGERBOT_DELAY}{Style.RESET_ALL}")
        print(
            f"        Aim Speed            : {Fore.CYAN}X: {AIM_SPEED_X} Y: {AIM_SPEED_Y}{Style.RESET_ALL}"
        )
        print(
            f"        Aim Offset           : {Fore.CYAN}X: {AIM_OFFSET_X} Y: {AIM_OFFSET_Y}{Style.RESET_ALL}"
        )
        print(
            f"        Aim Activated        : {(Fore.GREEN if bot.aimtoggled else Fore.RED)}{bot.aimtoggled}{Style.RESET_ALL}"
        )
        print(f"        Enemy Color          : {str(colorname + COLOR)}{Style.RESET_ALL}")
        print("        ======================")
        print(
            f"{Style.BRIGHT}{Fore.CYAN}"
            "\nJoin the Discord: discord.gg/thunderclient !\n"
            "If this isn't from github.com/Seconb/Roblox-Colorbot, it's not legit!"
            f"{Style.RESET_ALL}"
        )
    except Exception as e:
        print("Error printing banner:", e)
        log_error(e)
        exit()

if __name__ == "__main__":
    bot = trbot()
    root = tk.Tk()
    root.withdraw()
    system('mode con: cols=54 lines=30')

    if SHOW_FOV.lower() == "enabled":
        create_circle(CAM_FOV // 2, (CAM_FOV_COLOR), 255)
        create_circle(AIM_FOV // 2, (AIM_FOV_COLOR), 255)

    toggle_thread = Thread(target=bot.togglebot)
    toggle_thread.start()
    try:
        print_banner(bot)
        while True:
            root.update()
            if SWITCH_MODE_KEY != "disabled" and is_pressed(SWITCH_MODE_KEY):
                bot.modeswitch()
                print_banner(bot)
            if FOV_KEY_UP != "disabled" and is_pressed(FOV_KEY_UP):
                change_config_setting("AIM_FOV", AIM_FOV+5)
                print_banner(bot)
            if FOV_KEY_DOWN != "disabled" and is_pressed(FOV_KEY_DOWN):
                change_config_setting("AIM_FOV", AIM_FOV-5)
                print_banner(bot)
            if UPDATE_KEY != "disabled" and is_pressed(UPDATE_KEY):
                load()
                if SHOW_FOV.lower() == "enabled":
                    root.destroy()
                    root = tk.Tk()
                    root.withdraw()
                    create_circle(CAM_FOV // 2, (CAM_FOV_COLOR), 255)
                    create_circle(AIM_FOV // 2, (AIM_FOV_COLOR), 255)
                    bot.switchmode = TOGGLE_HOLD_MODE
                print_banner(bot)

            sleep(0.01)
    except Exception as e:
        print("An error occurred:", e)
        log_error(e)
        exit()
