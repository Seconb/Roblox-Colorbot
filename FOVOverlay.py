
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
class FOVOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.overlays = []
        
    def create_circle_overlay(self, radius, color, alpha=255):
        image = Image.new('RGBA', (radius*2, radius*2), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse(
            (0, 0, radius*2-1, radius*2-1),
            outline=color + (alpha,),
            width=2
        )
        return image
    
    def show(self, cam_radius, aim_radius, cam_color, aim_color):
        self.clear()
        
        # Create camera FOV overlay
        cam_image = self.create_circle_overlay(cam_radius, cam_color)
        cam_photo = ImageTk.PhotoImage(cam_image)
        cam_window = self.create_overlay_window(cam_radius)
        cam_label = tk.Label(cam_window, image=cam_photo, bg='black')
        cam_label.image = cam_photo # type: ignore
        cam_label.pack()
        self.overlays.append(cam_window)
        
        # Create the aim FOV overlay
        aim_image = self.create_circle_overlay(aim_radius, aim_color)
        aim_photo = ImageTk.PhotoImage(aim_image)
        aim_window = self.create_overlay_window(aim_radius)
        aim_label = tk.Label(aim_window, image=aim_photo, bg='black')
        aim_label.image = aim_photo # type: ignore
        aim_label.pack()
        self.overlays.append(aim_window)
    
    def create_overlay_window(self, radius):
        window = tk.Toplevel(self.root)
        window.overrideredirect(True)
        window.attributes('-topmost', True)
        window.attributes('-transparentcolor', 'black')
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window.geometry(f'+{(screen_width - radius*2)//2}+{(screen_height - radius*2)//2}')
        return window

    def clear(self):
        for overlay in self.overlays:
            try:
                overlay.destroy()
            except tk.TclError:
                pass
        self.overlays = []
    
    def update(self):
        self.root.update()
