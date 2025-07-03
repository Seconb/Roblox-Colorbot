
import numpy as np
import sys
from keybinds import *
from threading import Thread
from colorama import Fore, Style
from time import sleep, strftime, localtime
from keyboard import is_pressed
from os import system

# Initialize system
system("title Colorbot")
kernel = np.ones((3, 3), np.uint8)
TOGGLE_HOLD_MODES = ("Hold", "Toggle")
ERROR_LOG_PATH = "log.txt"

# error logging
def log_error(error_message):
    timestamp = strftime('%Y-%m-%d %H:%M:%S', localtime())
    try:
        with open(ERROR_LOG_PATH, "a") as log_file:
            log_file.write(f"{timestamp}: {error_message}\n")
    except Exception:
        with open(ERROR_LOG_PATH, "w") as log_file:
            log_file.write(f"{timestamp}: {error_message}\n")

def print_banner(bot):
    cfg = bot.cfg
    system("cls")
    
    # Banner
    print(Style.BRIGHT + Fore.CYAN + r'''
     ▄▄·       ▄▄▌        ▄▄▄  ▄▄▄▄·       ▄▄▄▄▄
    ▐█ ▌▪▪     ██•  ▪     ▀▄ █·▐█ ▀█▪▪     •██  
    ██ ▄▄ ▄█▀▄ ██▪   ▄█▀▄ ▐▀▀▄ ▐█▀▀█▄ ▄█▀▄  ▐█.▪
    ▐███▌▐█▌.▐▌▐█▌▐▌▐█▌.▐▌▐█•█▌██▄▪▐█▐█▌.▐▌ ▐█▌·
    ·▀▀▀  ▀█▄▀▪.▀▀▀  ▀█▄▀▪.▀  ▀·▀▀▀▀  ▀█▄▀▪ ▀▀▀ 
    ''' + Style.RESET_ALL)
    
    # Controls
    print("        ====== Controls ======")
    print(f"        Activate colorbot    : {Fore.YELLOW}{cfg.aim_key}{Style.RESET_ALL}")
    if cfg.switch_mode_key != "disabled":
        print(f"        Switch toggle/hold   : {Fore.YELLOW}{cfg.switch_mode_key}{Style.RESET_ALL}")
    if cfg.update_key != "disabled":
        print(f"        Update Config        : {Fore.YELLOW}{cfg.update_key}{Style.RESET_ALL}")
    if cfg.fov_key_up != "disabled" and cfg.fov_key_down != "disabled":
        print(f"        Change FOV           : {Fore.YELLOW}{cfg.fov_key_up}/{cfg.fov_key_down}{Style.RESET_ALL}")
    
    # Information
    print("        ==== Information =====")
    print(f"        Toggle/Hold Mode     : {Fore.CYAN}{TOGGLE_HOLD_MODES[cfg.toggle_mode]}{Style.RESET_ALL}")
    print(f"        Aim FOV              : {Fore.CYAN}{cfg.aim_fov}{Style.RESET_ALL}")
    print(f"        Cam FOV              : {Fore.CYAN}{cfg.cam_fov}{Style.RESET_ALL}")
    
    # Triggerbot status
    trigger_status = f"{Fore.GREEN}On" if cfg.triggerbot.lower() != "disabled" else f"{Fore.RED}Off"
    print(f"        Triggerbot           : {trigger_status}{Style.RESET_ALL}")
    if cfg.triggerbot_delay > 0:
        print(f"        Triggerbot Delay     : {Fore.GREEN}{cfg.triggerbot_delay}{Style.RESET_ALL}")
    
    # Smoothing status
    smooth_status = f"{Fore.GREEN}On" if cfg.smoothing_enabled else f"{Fore.RED}Off"
    print(f"        Smoothening          : {smooth_status}{Style.RESET_ALL}")
    if cfg.smoothing_enabled:
        print(f"        Smoothening Factor   : {Fore.CYAN}{cfg.smooth_factor}{Style.RESET_ALL}")
    
    # Other settings
    print(f"        Aim Speed            : {Fore.CYAN}X: {cfg.aim_speed_x} Y: {cfg.aim_speed_y}{Style.RESET_ALL}")
    print(f"        Aim Offset           : {Fore.CYAN}X: {cfg.aim_offset_x} Y: {cfg.aim_offset_y}{Style.RESET_ALL}")
    
    # Activation status
    aim_status = f"{Fore.GREEN}True" if bot.aim_toggled else f"{Fore.RED}False"
    print(f"        Aim Activated        : {aim_status}{Style.RESET_ALL}")
    
    # Color info
    print(f"        Enemy Color          : {cfg.color_name}{cfg.config.get('Config', 'COLOR')}{Style.RESET_ALL}")
    print("        ======================")
    
    # Footer
    print(f"{Style.BRIGHT}{Fore.CYAN}")
    print("Join the Discord: discord.com/invite/K8gdWHthVw !")
    print("If this isn't from github.com/Seconb/Roblox-Colorbot, it's not legit!")
    print(f"{Style.RESET_ALL}")

def main():
    from config import ConfigManager
    cfg = ConfigManager()

    system('mode con: cols=54 lines=30')
    
    from FOVOverlay import FOVOverlay
    overlay = FOVOverlay()
    if cfg.show_fov.lower() == "enabled":
        overlay.show(cfg.cam_fov, cfg.aim_fov, cfg.cam_fov_color, cfg.aim_fov_color)
    
    from Colorbot import Colorbot
    bot = Colorbot(cfg)
    bot_thread = Thread(target=bot.run, daemon=True)
    bot_thread.start()
    
    print_banner(bot)
    
    try:
        while True:
            overlay.update()
            
            if cfg.switch_mode_key != "disabled" and is_pressed(cfg.switch_mode_key):
                bot.switch_mode()
                print_banner(bot)
            
            if cfg.fov_key_up != "disabled" and is_pressed(cfg.fov_key_up):
                cfg.update_setting("AIM_FOV", cfg.aim_fov + 5)
                print_banner(bot)
                
            if cfg.fov_key_down != "disabled" and is_pressed(cfg.fov_key_down):
                cfg.update_setting("AIM_FOV", cfg.aim_fov - 5)
                print_banner(bot)
            
            if cfg.update_key != "disabled" and is_pressed(cfg.update_key):
                cfg.load()
                if cfg.show_fov.lower() == "enabled":
                    overlay.show(cfg.cam_fov, cfg.aim_fov, cfg.cam_fov_color, cfg.aim_fov_color)
                print_banner(bot)
            
            sleep(0.01)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        log_error(f"Main loop error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()