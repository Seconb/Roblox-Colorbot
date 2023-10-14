import keyboard
import time
import PIL.ImageGrab
import PIL.Image
import winsound
import os
import mss
import configparser
import cv2
import numpy as np
import threading
import time
import win32api
import win32con
from colorama import Fore, Style, init
import ctypes

switchmodes = ["hold", "toggle"]
mods = ["slow", "medium", "fast", "burst"]


class FoundEnemy(Exception):
    pass


sdir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(sdir, "config.ini")
config = configparser.ConfigParser()
config.optionxform = str
config.read(config_file_path)


def loadsettings():

    global A1M_KEY, SWITCH_MODE_KEY, FOV_KEY_UP, FOV_KEY_DOWN, CAM_FOV, A1M_OFFSET_Y, A1M_OFFSET_X, A1M_SPEED_X, A1M_SPEED_Y
    global COLOR, upper, lower, A1M_FOV

    A1M_KEY_STRING = config.get("Config", "A1M_KEY")
    if "win32con" in A1M_KEY_STRING:
        A1M_KEY = eval(A1M_KEY_STRING, {"win32con": win32con})
    else:
        A1M_KEY = str(A1M_KEY_STRING)
    COLOR = config.get("Config", "COLOR")
    SWITCH_MODE_KEY = config.get("Config", "SWITCH_MODE_KEY")
    FOV_KEY_UP = config.get("Config", "FOV_KEY_UP")
    FOV_KEY_DOWN = config.get("Config", "FOV_KEY_DOWN")
    CAM_FOV = int(config.get("Config", "CAM_FOV"))
    A1M_FOV = int(config.get("Config", "A1M_FOV"))
    A1M_OFFSET_Y = int(config.get("Config", "A1M_OFFSET_Y"))
    A1M_OFFSET_X = int(config.get("Config", "A1M_OFFSET_X"))
    A1M_SPEED_X = float(config.get("Config", "A1M_SPEED_X"))
    A1M_SPEED_Y = float(config.get("Config", "A1M_SPEED_Y"))
    if COLOR.lower() == "purple":
        upper = np.array([155, 255, 255], dtype="uint8")
        lower = np.array([130, 50, 195], dtype="uint8")
    if COLOR.lower() == "yellow":
        upper = np.array([38, 255, 203], dtype="uint8")
        lower = np.array([30, 255, 201], dtype="uint8")
    if COLOR.lower() == "red":
        # prototype1 upper = np.array([179, 244, 255], dtype='uint8')
        # lower = np.array([0, 91, 195], dtype='uint8')
        # SHIT PROTO upper = np.array([179, 244, 255], dtype='uint8')
        # lower = np.array([0, 91, 195], dtype='uint8')
        # upper = np.array([0, 255, 255], dtype='uint8')
        # lower = np.array([0, 174, 16], dtype='uint8')
        upper = np.array([4, 255, 255], dtype="uint8")
        lower = np.array([0, 255, 255], dtype="uint8")


def save():
    config.set("Config", "CAM_FOV", str(CAM_FOV))
    config.set("Config", "A1M_SPEED_X", str(A1M_SPEED_X))
    config.set("Config", "A1M_SPEED_Y", str(A1M_SPEED_Y))
    with open(config_file_path, "w") as configfile:
        config.write(configfile)


sct = mss.mss()

loadsettings()
screenshot = sct.monitors[1]
screenshot["left"] = int((screenshot["width"] / 2) - (CAM_FOV / 2))
screenshot["top"] = int((screenshot["height"] / 2) - (CAM_FOV / 2))
screenshot["width"] = CAM_FOV
screenshot["height"] = CAM_FOV
center = CAM_FOV / 2

audiodir = os.path.join(sdir, "audio")


def audio(wavname):
    audiopath = os.path.join(audiodir, wavname)
    winsound.PlaySound(audiopath, winsound.SND_FILENAME)


def lclc():
    return win32api.GetAsyncKeyState(A1M_KEY) < 0


class trb0t:
    def __init__(self):
        self.a1mtoggled = False
        self.mode = 2
        self.switchmode = 0

    def run(self):
        if self.a1mtoggled:
            self.process()

    def process(self):
        timestart = time.time()
        while lclc():
            img = np.array(sct.grab(screenshot))
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower, upper)
            kernel = np.ones((3, 3), np.uint8)
            dilated = cv2.dilate(mask, kernel, iterations=5)
            thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
            (contours, hierarchy) = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
            )
            contour_img = np.zeros_like(img)
            if len(contours) != 0:
                timeend = time.time()
                contour = max(contours, key=cv2.contourArea)
                topmost = tuple(contour[contour[:, :, 1].argmin()][0])
                x = topmost[0] - center + A1M_OFFSET_X
                y = topmost[1] - center + A1M_OFFSET_Y
                distance = np.sqrt(x ** 2 + y ** 2)
                if (distance <= A1M_FOV):
                    x2 = x * A1M_SPEED_X
                    y2 = y * A1M_SPEED_Y
                    x2 = int(x2)
                    y2 = int(y2)
                    ctypes.windll.user32.mouse_event(0x0001, x2, y2, 0, 0)
                else:
                    break

    def a1mtoggle(self):
        self.a1mtoggled = not self.a1mtoggled

    def modeswitch(self):
        if self.switchmode == 0:
            self.switchmode += 1
            audio("toggle.wav")
        elif self.switchmode == 1:
            self.switchmode -= 1
            audio("hold.wav")


def print_banner(b0t: trb0t):
    os.system("cls")
    colorm = ""
    if COLOR.lower() == "red":
        colorm = f"{Fore.RED}{COLOR}{Style.RESET_ALL}"
    elif COLOR.lower() == "yellow":
        colorm = f"{Fore.YELLOW}{COLOR}{Style.RESET_ALL}"
    elif COLOR.lower() == "purple":
        colorm = f"{Fore.MAGENTA}{COLOR}{Style.RESET_ALL}"
    else:
        colorm = str(COLOR)
    print(Style.BRIGHT + Fore.CYAN + """ AMBATUAIM v1.5 """ + Style.RESET_ALL)
    print("====== Controls ======")
    print("Activate a1mb0t      :", Fore.YELLOW + str(A1M_KEY) + Style.RESET_ALL)
    print("Switch toggle/hold   :", Fore.YELLOW + SWITCH_MODE_KEY + Style.RESET_ALL)
    print(
        "Change FOV           :",
        Fore.YELLOW + FOV_KEY_UP + "/" + FOV_KEY_DOWN + Style.RESET_ALL,
    )
    print("==== Information =====")
    print(
        "Toggle/Hold Mode     :",
        Fore.CYAN + switchmodes[b0t.switchmode] + Style.RESET_ALL,
    )
    print("A1m FOV              :", Fore.CYAN + str(A1M_FOV) + Style.RESET_ALL)
    print("Cam FOV              :", Fore.CYAN + str(CAM_FOV) + Style.RESET_ALL)
    print(
        "A1m Speed            :",
        Fore.CYAN
        + "X: "
        + str(A1M_SPEED_X)
        + " Y: "
        + str(A1M_SPEED_Y)
        + Style.RESET_ALL,
    )
    print(
        "A1m Offset           :",
        Fore.CYAN
        + "X: "
        + str(A1M_OFFSET_X)
        + " Y: "
        + str(A1M_OFFSET_Y)
        + Style.RESET_ALL,
    )
    print(f"Enemy Color          : {colorm}" + Style.RESET_ALL)
    print(
        "A1m Activated        :",
        (Fore.GREEN if b0t.a1mtoggled else Fore.RED)
        + str(b0t.a1mtoggled)
        + Style.RESET_ALL,
    )


if __name__ == "__main__":
    b0t = trb0t()
    print_banner(b0t)
    ot = time.time()
    while True:
        if SWITCH_MODE_KEY != "disabled" and keyboard.is_pressed(SWITCH_MODE_KEY):
            b0t.modeswitch()
            print_banner(b0t)
        if FOV_KEY_UP != "disabled" and keyboard.is_pressed(FOV_KEY_UP):
            A1M_FOV += 5
            audio("fovup.wav")
            print_banner(b0t)
        if FOV_KEY_DOWN != "disabled" and keyboard.is_pressed(FOV_KEY_DOWN):
            A1M_FOV -= 5
            audio("fovdown.wav")
            print_banner(b0t)

        time.sleep(0.01)

        if lclc():
            if b0t.switchmode == 0:
                while lclc():
                    if not b0t.a1mtoggled:
                        b0t.a1mtoggle()
                        print_banner(b0t)
                        while b0t.a1mtoggled:
                            b0t.run()
                            if not lclc():
                                b0t.a1mtoggle()
                                print_banner(b0t)
            if b0t.switchmode == 1:
                b0t.a1mtoggle()
                print_banner(b0t)
                winsound.Beep(200, 200)
                while b0t.a1mtoggled and not keyboard.is_pressed(A1M_KEY):
                    b0t.run()

#weghfwe78pfgwe78fgwe78fegw78fg8w7egfwedgwepg8o234hg89p234hg8923hg8923hfgeuipwgbqeuoahgbreyuiogbu80qeyrghy80qewgbo8