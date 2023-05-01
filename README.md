# Kindlefusion 
Tested on kindle4

A setup to allow for generating images from kindle books with minimal interuption. Highlighting the text and then clicking ok will download and display an image using Stable Diffusion via StableHorde https://stablehorde.net/ . 

Youtube explanation video:
<BR>
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/SueGVpyrgG8/0.jpg)](https://www.youtube.com/watch?v=SueGVpyrgG8)

Mobileread thread: https://www.mobileread.com/forums/showthread.php?t=352505

Now with extra feature creep of:
- Gallery to view and select past images
- Upload box to show image
- Manual search in Stable diffusion and Unsplash for a given search term
- Mobile phone camera in the form of a local html file which passes an image directly to the kindle

A personal project but it might be of interest to others too. I will likely also use it (without the checking for highlights) as a picture frame that can change based on voice inputs. I have another project that us set up for adding and displaying notes / to do lists, and may look at may look at merging that in at a later date.

**Disclaimer: This project is a work in progress and may contain bugs or incomplete features.
My concerns currently would be the effect of constantly checking the clippings file, or the risk potentially filling up a kindle with images. Very open to suggestions or advice with this**

Note that this version is set up to use Stablehorde, but I previously made it for use with local Automatic1111 and can look at merging that code if it is of interest

Please note that this could be simplified with an updated version of pillow, ffmpeg, imagemagick, or with the library webp, but I have struggled getting cross compilation working, and would appreciate advice for that. Currently it has a separate api endpoint whos sole purpose is to take in a heic webp in the form of a png and return it as a png/jpg. I am using jpg currently.

## Installation

To install this project, follow these steps:

1. Install the required libraries that I haven't got round to listing yet
2. Move the files in the "add_to_kindle" folder onto a kindle
3. Add your stable horde key from https://stablehorde.net/register to secret_config.json. Without this you will be lower priority so the image generation will take longer.
4. If you want to use the camera from a mobile, then copy the camera folder to it. I had to put it into the download folder for opera at file:///sdcard/Android/data/com.opera.browser/files/Download/cam/caaam5.html . This is not necessary and is just feature creep, but cool to see the images being sent to the kindle.



## How to Run

To run this project, follow these steps:

1. Make sure you're in the project directory.
2. Open port 5000 if you want to access the helper page via wifi. This is done with the command "iptables -A INPUT -p tcp --dport 5000 -i wlan0 -j ACCEPT"
3. Run "python3 stable11.py"
5. Now either heighlight some text and when you click finish, it will send that off to stable diffusion and bring back an image for you. In my experience this is between around 5 seconds and around 30 seconds, however the API must be running on the remote server due to the webp file. This is not currently running but you can run your own. I need to get some feedback as to whether it is secure enough for hosting on the net. In the longrun I would like to replace this with using a compiled webp binary on the kindle itself.
4. To clear the image just click to change the page. Note that all generated pics are saved to the /gallery/images folder. 
5. For additional functionality (or to see / load previous images) , open your web browser and navigate to `http://your_kindle_ip:5000`.

Note that this will spam up your highlights, so you might want to back that up if you don't want to have to clear it out afterwards

## Previews

Here are some previews of the interface:


<strong>Generating from a book:</strong>
<div style="border: 1px solid black; padding: 5px; display: inline-block;">
  <img src="/documentation/lookup.png" alt="Interface Preview" style="max-width: 50%; height: auto;">
</div>
<br>
<strong>Web interface:</strong>
<div style="border: 1px solid black; padding: 5px; display: inline-block;">
  <img src="/documentation/interface.png" alt="Interface Preview" style="max-width: 50%; height: auto;">
</div>
<br>
<strong>Selecting from gallery:</strong>
<div style="border: 1px solid black; padding: 5px; display: inline-block;">
  <img src="/documentation/gallery.png" alt="Gallery Preview" style="max-width: 50%; height: auto;">
</div>
<br>
<strong>Use of the mobile html camera "app"</strong>
<div style="border: 1px solid black; padding: 5px; display: inline-block;">
  <img src="/documentation/camera.png" alt="Camera Preview" style="max-width: 50%; height: auto;">
</div>
<strong>Mounted into picture frames</strong>
<div style="border: 1px solid black; padding: 5px; display: inline-block;">
  <img src="/documentation/1682950016238.jpeg" alt="Camera Preview" style="max-width: 50%; height: auto;">
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
