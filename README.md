# Kindlefusion

**Disclaimer: This project is a work in progress and may contain bugs or incomplete features.**

## Installation

To install this project, follow these steps:

1. Install the required libraries that I haven't got round to listing yet
2. Move the files in the "add_to_kindle" folder onto a kindle
3. Add your stable horde key from https://stablehorde.net/register to secret_config.json. Without this you will be lower priority so the image generation will take longer.
4. If you want to use the camera from a mobile, then copy the camera folder to it. I had to put it into the download folder for opera at file:///sdcard/Android/data/com.opera.browser/files/Download/cam/caaam5.html . This is not necessary and is just feature creep, but it's also pretty fun.



## How to Run

To run this project, follow these steps:

1. Make sure you're in the project directory.
2. Open port 5000 if you want to access the helper page via wifi. This is done with the command "iptables -A INPUT -p tcp --dport 5000 -i wlan0 -j ACCEPT"
3. Run "python3 stable11.py"
5. Now either heighlight some text and when you click finish, it will send that off to stable diffusion and bring back an image for you. In my experience this is between around 5 seconds and around 30 seconds, however the API must be running on the remote server due to the webp file. This is not currently running but you can run your own. I need to get some feedback as to whether it is secure enough for hosting on the net. In the longrun I would like to replace this with using a compiled webp binary on the kindle itself.
4. For additional functionality, open your web browser and navigate to `http://your_kindle_ip:5000`.


## Guide

The original goal was to have it so that selecting text and then clicking ok will do a lookup for you. This works, but I have had feature creep since then, so there are also now options to

-Search in Stable diffision and Unsplash for a given search term
-upload an image to display
-view and select past images from gallery





## Credits

This project was created by [diggedypomme](https://github.com/diggedypomme). 

It makes use of:

-StableHorde https://stablehorde.net/ for image generation
-Ai Horde by db0 - https://github.com/db0/AI-Horde - Python interface for stable horde
-Unsplash  - https://unsplash.com/ - For simple gallery lookup
-NiLuJe  - https://github.com/NiLuJe/FBInk - FBInk display library
-NiLuJe  - https://github.com/NiLuJe/py-fbink - FBInk display library python interface
-NiLuJe  - https://www.mobileread.com/forums/showthread.php?t=225030 - FBInk jailbreak and many other files.


