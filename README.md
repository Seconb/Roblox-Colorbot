# THIS PROJECT WILL NO LONGER RECEIVE MAINTENANCE OR SUPPORT
- The colorbot is currently broken for unknown reasons.
- For those attempting to fix it, my troubleshooting so far has found: Everything works except when the script checks if any enemies are in the image, it never finds them. (if len(contours) != 0: never returns true)
- The enemy outline colors are still accurate, the screenshotting system works and takes correct screenshots, it isn't an issue with checking if the user has Roblox focused, and it isn't that Roblox began blocking mouse_event.

# WIKI
- See the wiki for a full usage guide and other usage information (i.e Troubleshooting).
- https://github.com/Seconb/Roblox-Colorbot/wiki

# CREDITS

- Seconb (Primary developer)
- AndrewDarkyy (https://github.com/AndrewDarkyy) (https://discord.com/invite/K8gdWHthVw) (Co-developer, contributed many features such as triggerbot, smoothening, version checker, and optimizations)
- Befia/Taylor (Contributed some bugfixes and comments to explain certain areas of code, and added basic error handling. Not an actual developer for the project though)
- Hariangr for their HSVRangeTool (https://github.com/hariangr/HsvRangeTool)
- PossibIy (Contributed the Show FOV feature) (https://github.com/possibIy)

# FEATURES

- Colorbot based on the outlines around enemies in some Roblox games, namely: Arsenal, Aimblox, and Bad Business
- Custom color feature which allows for multi-game support.
- Triggerbot (automatically shoots enemies if enabled!)
- Adjustable aim (where it aims like their head or their body, and the speed and distance it does that from)
- Easy configuration via a file!
- Many choices for enemy outline colors!
