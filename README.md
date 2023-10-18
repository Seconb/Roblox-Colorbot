# Arsenal-Colorbot
A neat little colorbot that uses enemy outlines for Arsenal. Ported from my Valorant colorbot with mouse input method modified.

Troubleshooting Guide:

https://streamable.com/xcbfez

Usage Tutorial:

- Set settings to be as follows (doesn't need to be exact, these are just what I recommend):

https://i.imgur.com/Wxs9JKy.png

https://i.imgur.com/IAFsqwl.png



The enemy outline is actually necessary other settings don't matter as much.



You can enter the settings menu from the gear in the bottom left of the menu.



Config Guide:




- For keybinds, if you're just using a button on your keyboard like A, B, C, Shift, or something like CTRL+ALT+Q, then set "BINDMODE" to keyboard

- If you're using side mouse button, set it to win32 so you can use win32api and use these keycodes, formatting would look like: A1M_KEY = win32con.VK_XBUTTON2

- The other keys will only be able to be bound to keyboard.

- FOV_KEY_UP and DOWN do exactly as they say. Increase or decrease FOV in increments of 5.

- CAM_FOV is the size of screenshot the bot takes. Basically, it takes screenshots constantly and reads through them to look for yellow. This determines the box it will search. It will only aim for targets it finds within the FOV you set, however. I recommend you keep it on default if you play on 1920 x 1080, though results differ on different resolutions. The only reason why it's done like this is to prevent bugs.

- A1M_SPEED_X and Y control the speed. It differs based on your DPI and general sensitivity settings.

- A1M_OFFSET_X and Y will offset the aim by a set amount of pixels. Usually, it'll aim for the first enemy color it finds in the screenshot, so it's the most top left part of the enemy. By default, it will move 7 pixels right of that and 10 pixels down to get the center of the head. Do not change this if it works fine by default or if you don't know what you're doing.



Once you're configured, run the script and you're good.
