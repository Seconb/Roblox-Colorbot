from main import log_error, print_banner, kernel
import cv2
import numpy as np
import win32api
from threading import Thread
from time import sleep
import pygetwindow as gw
from keyboard import is_pressed
from keybinds import *
from FOVOverlay import FOVOverlay
from config import ConfigManager


class Colorbot:
    def __init__(self, config):
        self.cfg = config
        self.aim_toggled = False
        self.clicks = 0
        self.shooting = False

    def is_roblox_focused(self):
        try:
            return gw.getActiveWindow().title == "Roblox" # type: ignore
        except (AttributeError, TypeError):
            return False
        except Exception as e:
            log_error(f"Window focus error: {e}")
            return False

    def process_frame(self):
        if not self.is_roblox_focused():
            return
            
        try:
            if self.cfg.cam_type.lower() == "bettercam":
                frame = self.cfg.camera.grab(region=self.cfg.region)
            else:
                frame = np.array(self.cfg.sct.grab(self.cfg.screenshot_area))
            
            if frame is None:
                return
                
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, self.cfg.lower, self.cfg.upper)
            dilated = cv2.dilate(mask, kernel, iterations=5)
            _, thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            
            if not contours:
                return
                
            largest_contour = max(contours, key=cv2.contourArea)
            top_point = tuple(largest_contour[largest_contour[:, :, 1].argmin()][0])
            
            rel_x = top_point[0] - self.cfg.center + self.cfg.aim_offset_x
            rel_y = top_point[1] - self.cfg.center + self.cfg.aim_offset_y
            distance = (rel_x**2 + rel_y**2)**0.5
            
            if distance > self.cfg.aim_fov:
                return
                
            move_x = int(rel_x * self.cfg.aim_speed_x)
            move_y = int(rel_y * self.cfg.aim_speed_y)
            
            if (self.cfg.smoothing_enabled and distance >= self.cfg.smooth_factor) or not self.cfg.smoothing_enabled:
                    if move_x or move_y: # dont move if theres nothing to move lol
                        win32api.mouse_event(0x0001, move_x, move_y, 0, 0)

            
            if self.cfg.triggerbot.lower() != "disabled" and distance <= self.cfg.triggerbot_distance:
                if self.cfg.triggerbot_delay > 0:
                    if not self.shooting:
                        Thread(target=self.delayed_trigger).start()
                else:
                    self.trigger_shot()
        except Exception as e:
            log_error(f"Processing error: {e}")
    
    def trigger_shot(self):
        if not self.shooting:
            self.shooting = True
            win32api.mouse_event(0x0002, 0, 0, 0, 0)
            self.clicks += 1
            Thread(target=self.release_trigger).start()
            self.shooting = False

    
    def release_trigger(self):
        current_clicks = self.clicks
        sleep(0.05)
        if self.clicks == current_clicks:
            win32api.mouse_event(0x0004, 0, 0, 0, 0)
    
    def delayed_trigger(self):
        self.shooting = True
        sleep(self.cfg.triggerbot_delay / 1000)
        self.trigger_shot()
        self.shooting = False
    
    def toggle_aim(self):
        self.aim_toggled = not self.aim_toggled
        sleep(0.15)
    
    def switch_mode(self):
        self.cfg.toggle_mode = 1 - self.cfg.toggle_mode
        sleep(0.15)
    
    def run(self):
        while True:
            if is_pressed(self.cfg.aim_key):
                # Hold mode
                if self.cfg.toggle_mode == 0 and not self.aim_toggled:
                    self.toggle_aim()
                    print_banner(self)
                    while is_pressed(self.cfg.aim_key) and self.aim_toggled:
                        self.process_frame()
                    if not is_pressed(self.cfg.aim_key):
                        self.toggle_aim()
                        print_banner(self)
                # Toggle mode
                elif self.cfg.toggle_mode == 1:
                    self.toggle_aim()
                    print_banner(self)
                    while self.aim_toggled:
                        self.process_frame()
                        if is_pressed(self.cfg.aim_key):
                            self.toggle_aim()
                            print_banner(self)
            sleep(0.01)
