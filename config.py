
import configparser
from os import system, chdir
from os.path import dirname, join
from colorama import Fore, Style
import sys
import numpy as np
import win32api

class ConfigManager:
    def __init__(self):
        self.config_file = self.get_config_path()
        self.config = configparser.ConfigParser()
        self.config.optionxform = str # type: ignore 
        self.load()
        
    def get_config_path(self):
        if getattr(sys, 'frozen', False):
            app_path = dirname(sys.executable)
            chdir(app_path)
            return join(app_path, 'config.txt')
        else:
            script_dir = dirname(__file__)
            chdir(script_dir)
            return join(script_dir, "config.txt")
    
    def load(self):
        self.config.read(self.config_file)
        self.process_settings()
        
    def process_settings(self):
        # Core settings
        self.aim_key = self.config.get("Config", "AIM_KEY")
        self.switch_mode_key = self.config.get("Config", "SWITCH_MODE_KEY")
        self.update_key = self.config.get("Config", "UPDATE_KEY")
        self.fov_key_up = self.config.get("Config", "FOV_KEY_UP")
        self.fov_key_down = self.config.get("Config", "FOV_KEY_DOWN")
        
        # Numerical settings
        self.cam_fov = int(self.config.get("Config", "CAM_FOV"))
        self.aim_fov = int(self.config.get("Config", "AIM_FOV"))
        self.aim_offset_y = int(self.config.get("Config", "AIM_OFFSET_Y"))
        self.aim_offset_x = int(self.config.get("Config", "AIM_OFFSET_X"))
        self.aim_speed_x = float(self.config.get("Config", "AIM_SPEED_X"))
        self.aim_speed_y = float(self.config.get("Config", "AIM_SPEED_Y"))
        self.triggerbot_delay = int(self.config.get("Config", "TRIGGERBOT_DELAY"))
        self.triggerbot_distance = int(self.config.get("Config", "TRIGGERBOT_DISTANCE"))
        self.smooth_factor = float(self.config.get("Config", "SMOOTH_FACTOR"))
        
        # True/False settings
        self.triggerbot = self.config.get("Config", "TRIGGERBOT")
        self.smoothing = self.config.get("Config", "SMOOTHENING")
        self.hide_console = self.config.get("Config", "HIDE_CONSOLE")
        self.show_fov = self.config.get("Config", "SHOW_FOV")
        self.cam_type = self.config.get("Config", "CAM_TYPE")
        self.toggle_hold_mode = self.config.get("Config", "TOGGLE_HOLD_MODE")
        self.center = self.cam_fov / 2
        
        # Color settings
        self.cam_fov_color = tuple(map(int, self.config.get("Config", "CAM_FOV_COLOR").split(', ')))
        self.aim_fov_color = tuple(map(int, self.config.get("Config", "AIM_FOV_COLOR").split(', ')))
        upper_color = tuple(map(int, self.config.get("Config", "UPPER_COLOR").split(', ')))
        lower_color = tuple(map(int, self.config.get("Config", "LOWER_COLOR").split(', ')))

        # modes
        self.toggle_mode = 0 if self.toggle_hold_mode.lower() == "hold" else 1
        self.smoothing_enabled = self.smoothing.lower() != "disabled" and self.smooth_factor > 0
        
        self.init_camera()
        
        if self.hide_console.lower() == "enabled":
            self.hide_console_window()
        
        self.color_name, self.upper, self.lower = self.get_color_settings(
            self.config.get("Config", "COLOR"),
            upper_color,
            lower_color
        )
    
    # separate the color settings logic for better readability
    # looks much cleaner - taylor
    def get_color_settings(self, color_name, upper_color, lower_color):
        color_map = {
            "yellow": (Fore.YELLOW, np.array((30, 255, 229)), np.array((30, 255, 229))),
            "blue": (Fore.BLUE, np.array((120, 255, 229)), np.array((120, 255, 229))),
            "pink": (Fore.MAGENTA, np.array((150, 255, 229)), np.array((150, 255, 229))),
            "magenta": (Fore.MAGENTA, np.array((150, 255, 229)), np.array((150, 255, 229))),
            "purple": (Fore.MAGENTA, np.array((150, 255, 229)), np.array((150, 255, 229))),
            "green": (Fore.GREEN, np.array((60, 255, 229)), np.array((60, 255, 229))),
            "cyan": (Fore.CYAN, np.array((90, 255, 229)), np.array((90, 255, 229))),
            "red": (Fore.RED, np.array((0, 255, 229)), np.array((0, 255, 229))),
            "custom": (Fore.WHITE, np.array(upper_color), np.array(lower_color)),
            "0000ff": (Fore.BLUE, np.array((123, 255, 255)), np.array((120, 147, 69))),
            "aimblox": (Fore.LIGHTRED_EX, np.array((4, 225, 206)), np.array((0, 175, 119))),
            "black": (Fore.WHITE, np.array((0, 0, 0)), np.array((0, 0, 0))),
        }
        return color_map.get(color_name.lower(), (Fore.WHITE, np.array(upper_color), np.array(lower_color)))
    
    def init_camera(self): # pick capturing method
        if self.cam_type.lower() == "mss":
            import mss
            self.sct = mss.mss()
            monitor = self.sct.monitors[1]
            self.screenshot_area = {
                "left": int((monitor["width"] / 2) - (self.cam_fov / 2)),
                "top": int((monitor["height"] / 2) - (self.cam_fov / 2)),
                "width": self.cam_fov,
                "height": self.cam_fov
            }
        else:
            import bettercam
            screen_width = win32api.GetSystemMetrics(0)
            screen_height = win32api.GetSystemMetrics(1)
            left = (screen_width - self.cam_fov) // 2
            top = (screen_height - self.cam_fov) // 2
            self.region = (left, top, left + self.cam_fov, top + self.cam_fov)
            self.camera = bettercam.create(output_idx=0, output_color="BGR")
    
    def hide_console_window(self):
        try:
            import ctypes
            import win32gui
            console_window = ctypes.windll.kernel32.GetConsoleWindow()
            if console_window != 0:
                ctypes.windll.user32.ShowWindow(console_window, 0)
                win32gui.ShowWindow(console_window, 0)
        except Exception:
            pass
    
    def update_setting(self, setting, value):
        self.config.set("Config", setting, str(value))
        with open(self.config_file, "w") as config_file:
            self.config.write(config_file)
        self.load()
