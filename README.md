# Kindlefusion 

Version 17 (02/05/2023)
Tested on kindle 3 & kindle 4. I am currently in the process of updating the videos and imnages to match the latest version. 

This initially started as a project to allow highlighting of text within a kindle e-book to generate an image based on the text. This has since feature-crept and moved to acting as a picture frame that can receive images created via Stable Diffusion. The old version folder (https://github.com/diggedypomme/Kindlefusion/tree/main/Old%20version) has the initial readme and code if you want to do the highlighting thing, but that has been depreciated for now due to a change in focus.

<div style="border: 1px solid black; padding: 5px; display: inline-block;">
  <img src="/documentation/1682950016238.jpeg" alt="Camera Preview" style="max-width: 50%; height: auto;">
</div>
<BR>

Kindlefusion creates a html front end that can be used to upload images or get these from Stable Horde (https://stablehorde.net) / Automatic1111. A separate script can run on your pc monitoring the output folder of Automatic1111 and sending each image through to the Kindle. If using the mobile page then requesting an image via voice can also be used.


Youtube explanation video for the old version:
<BR>
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/SueGVpyrgG8/0.jpg)](https://www.youtube.com/watch?v=SueGVpyrgG8)

Mobileread thread: https://www.mobileread.com/forums/showthread.php?t=352505

Now with extra feature creep of:
- Gallery to view and select past images
- Upload box to show image
- Manual search in Stable diffusion and Unsplash for a given search term
- Mobile phone camera in the form of a local html file which passes an image directly to the kindle
- Voice commands
- Ability to disable screensaver

A personal project but it might be of interest to others too. 

**Disclaimer: This project is a work in progress and may contain bugs or incomplete features.
My concerns are 
- The risk potentially filling up a kindle with images. Shouldn't happen as there is a lot of space on the kindes, but I am not currently checking for this. Very open to suggestions or advice with this**
- It is running with a CORS override. Not sure how big of an issue this is - definitely don't open it to the net
- This does not use any power saving mode (sleeping inbetween image updates). I don't think I can have flask running at the same time if I do this, but again - open to suggestions


The front end now has a selection dropdown for the use of Stable Horde or Automatic1111. 

Stable Horde defaults to using JS to convert from webp as I cannot get webp compiled for the kindle. A dropdown menu exists for the old method of using a separate api endpoint whos sole purpose is to take in a heic webp in the form of a png and return it as a png/jpg. Please note that this could be simplified with an updated version of pillow, ffmpeg, imagemagick, or with the library webp, but this is not currently an option due to my issues with cross compilation.

## Installation

To install this project, follow these steps:

1. Root the kindle and install KUAL, USBnetworking, and python3 (see https://www.mobileread.com/forums/showthread.php?t=225030)
2. Move the files in the "add_to_kindle" folder onto a kindle. If you are doing this via usb, the files go into the root folder. Over ssh it would be in mnt/us/ , so mnt/us/kindlefusion  etc. This will add kindlefusion itself, as well as a launcher for KUAL.
3. Select "install libraries" from the kindlefusion menu in Kual. If this works, you can skip to step 4. If you have any issues getting this to run then issue the following commands over ssh:

3b. Install pip: "python3 -m ensurepip --upgrade"
3c. Install flask: "/mnt/us/python3/bin/pip3 install flask"
3d. Install loguru: "/mnt/us/python3/bin/pip3 install loguru"
3e. Install flask CORS: "/mnt/us/python3/bin/pip3 install flask_cors"
3f. make sure the clippings file exists: "touch  '/mnt/us/documents/My Clippings.txt'"

4. Add your stable horde key from https://stablehorde.net/register to secret_config.json (in the kindlefusion folder). Without this it will work, but will be lower priority so the image generation will take longer. A name for the kindle (which shows on boot) can also be added. This can also be added via the web ui but will need kindlefusion to be restarted
5. If you want to use the camera from a mobile, then copy caaam9.html and camera.png to it. I had to put it into the download folder for opera at file:///sdcard/Android/data/com.opera.browser/files/Download/cam/caaam9.html. This is not necessary if you don't want to use the mobile page, and actually most of the core functionality can be used without this, however it does add the ability to use voice to request the images (the browser voice request either needs ssl running on the flask app, or needs to be local to the device, hence this separate file)



## How to Run

To run the project, you can either do this via ssh, or via the KUAL menu. The KUAL menu would be the best way, but I will include the steps for running over SSH too:

Via KUAL:
1. Select "open 5000". This will open the port over wifi, as well as running "mntroot rw" to make the kindle file structure writeable.
2. Select "Start Kindlefusion"
3. Visit the kindles address which is listed at the top right of the flash screen (for example 192.168.0.10:5000 )

Over SSH:
1. Make sure you're in the project directory ("/mnt/us/kindlefusion")
2. Open port 5000 if you want to access the helper page via wifi. This is done with the command "iptables -A INPUT -p tcp --dport 5000 -i wlan0 -j ACCEPT"
3. Run "python3 stable17.py"
4. Visit the kindles address which is listed at the top right of the flash screen (for example 192.168.0.10:5000 )


## Previews

Here are some previews of the interface:


<strong>Generating from a book. Note that this is now disabled:</strong>
<div style="border: 1px solid black; padding: 5px; display: inline-block;">
  <img src="/documentation/lookup.png" alt="Interface Preview" style="max-width: 50%; height: auto;">
</div>
<br>
<strong>Old Web interface:</strong>
<div style="border: 1px solid black; padding: 5px; display: inline-block;">
  <img src="/documentation/interface.png" alt="Interface Preview" style="max-width: 50%; height: auto;">
</div>
<br>
<strong>Selecting from gallery:</strong>
<div style="border: 1px solid black; padding: 5px; display: inline-block;">
  <img src="/documentation/gallery.png" alt="Gallery Preview" style="max-width: 50%; height: auto;">
</div>
<br>
<strong>Use of the old mobile html camera "app"</strong>
<div style="border: 1px solid black; padding: 5px; display: inline-block;">
  <img src="/documentation/camera.png" alt="Camera Preview" style="max-width: 50%; height: auto;">
</div>






## Credits

This project was created by [diggedypomme](https://github.com/diggedypomme). 

It makes use of:

- StableHorde https://stablehorde.net/ for image generation
- AI Horde by db0 - https://github.com/db0/AI-Horde - Python interface for stable horde
- Unsplash  - https://unsplash.com/ - For simple gallery lookup
- NiLuJe  - https://github.com/NiLuJe/FBInk - FBInk display library
- NiLuJe  - https://github.com/NiLuJe/py-fbink - FBInk display library python interface
- NiLuJe  - https://www.mobileread.com/forums/showthread.php?t=225030 - Kindle tools
- ChatGPT - for help, suggestions and a migraine
