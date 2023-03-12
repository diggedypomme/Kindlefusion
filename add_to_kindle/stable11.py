# Kindlefusion

#enter Stable horde api key here:
#And auth for the web converter:

import json
with open('secret_config.json') as f:
    secret_config = json.load(f)


#Note that you can do it without this, but it defaults to a slower response
horde_api_key = secret_config['horde_api_key']

#auth for the webp converter
converter_auth = tuple(secret_config['converter_auth'])
#Hopefully I can do away with the whole converter part.





import requests,  os, time, argparse, base64
from cli_logger import logger, set_logger_verbosity, quiesce_logger, test_logger
from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageOps
from io import BytesIO
from requests.exceptions import ConnectionError
from flask import Flask,request,jsonify

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-n', '--amount', action="store", required=False, type=int, help="The amount of images to generate with this prompt")
arg_parser.add_argument('-p','--prompt', action="store", required=False, type=str, help="The prompt with which to generate images")
arg_parser.add_argument('-w', '--width', action="store", required=False, type=int, help="The width of the image to generate. Has to be a multiple of 64")
arg_parser.add_argument('-l', '--height', action="store", required=False, type=int, help="The height of the image to generate. Has to be a multiple of 64")
arg_parser.add_argument('-s', '--steps', action="store", required=False, type=int, help="The amount of steps to use for this generation")
arg_parser.add_argument('--api_key', type=str, action='store', required=False, help="The API Key to use to authenticate on the Horde. Get one in https://stablehorde.net")
arg_parser.add_argument('-f', '--filename', type=str, action='store', required=False, help="The filename to use to save the images. If more than 1 image is generated, the number of generation will be prepended")
arg_parser.add_argument('-v', '--verbosity', action='count', default=0, help="The default logging level is ERROR or higher. This value increases the amount of logging seen in your screen")
arg_parser.add_argument('-q', '--quiet', action='count', default=0, help="The default logging level is ERROR or higher. This value decreases the amount of logging seen in your screen")
arg_parser.add_argument('--horde', action="store", required=False, type=str, default="https://stablehorde.net", help="Use a different horde")
arg_parser.add_argument('--nsfw', action="store_true", default=False, required=False, help="Mark the request as NSFW. Only servers which allow NSFW will pick it up")
arg_parser.add_argument('--censor_nsfw', action="store_true", default=False, required=False, help="If the request is SFW, and the worker accidentaly generates NSFW, it will send back a censored image.")
arg_parser.add_argument('--trusted_workers', action="store_true", default=False, required=False, help="If true, the request will be sent only to trusted workers.")
arg_parser.add_argument('--source_image', action="store", required=False, type=str, help="When a file path is provided, will be used as the source for img2img")
arg_parser.add_argument('--source_processing', action="store", required=False, type=str, help="Can either be img2img, inpainting, or outpainting")
arg_parser.add_argument('--source_mask', action="store", required=False, type=str, help="When a file path is provided, will be used as the mask source for inpainting/outpainting")
args = arg_parser.parse_args()



import time
import requests

from multiprocessing import Process

app = Flask(__name__)
app.static_folder = 'gallery/images/'
app.static_url_path = '/static'
#import requests

# Load Pillow
#from PIL import Image, ImageDraw, ImageFont
import random
from random import randint

# Load the FBInk wrapper module
from _fbink import ffi, lib as FBInk

from io import BytesIO









# Let's check which FBInk version we're using...
# NOTE: ffi.string() returns a bytes on Python 3, not a str, hence the extra decode
print("Loaded FBInk {}".format(ffi.string(FBInk.fbink_version()).decode("ascii")))

# Setup the config...
fbink_cfg = ffi.new("FBInkConfig *")
fbink_cfg.is_centered = True
fbink_cfg.is_halfway = True
fbink_cfg.is_verbose = True
fbink_cfg.is_flashing = True


# path to the log file you want to tail
log_file = "/mnt/us/documents/My Clippings.txt"

# open the log file and seek to the end
with open(log_file, "r") as f:
    f.seek(0, 2)  # move the file pointer to the end of the file
    prev_log = f.read()  # read the entire file



webpage='''hello<BR>HELLO"


<!DOCTYPE html>
<html>
<body>

<h2>Shortcuts</h2>

<iframe src="demo_iframe.htm" name="iframe_a" height="30px" width="200px" title="Iframe Example"></iframe>


   <h1>Image Upload Example</h1>
    <form method="post" action="/uploadthen" enctype="multipart/form-data" target="iframe_a">
      <input type="file" name="image">
      <input type="submit" value="Upload">
    </form>



</html>'''




@app.route("/uploader")
def uploader():
    return(webpage)



@app.route("/")
def thehome():
   
    return(''' 
<!DOCTYPE html>
<html>
  <head>
    <title>Kindlefusion</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f1f1f1;
      }


h1 {
   text-align: center;
        margin: 20px 0;
  font-family: sans-serif;
  font-size: 3rem;
  letter-spacing: 2px;
  text-transform: uppercase;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);

color: #877c75;
}

h2 {
   text-align: center;
        margin: 20px 0;
  font-family: sans-serif;
  font-size: 1.5rem;
  letter-spacing: 2px;

  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
color: #898684;
}




      iframe {
        width: 70%;
        height: 200px;
        border: none;
        margin: 20px auto;
        display: block;
      }
      label, textarea {
        display: block;
        margin: 20px auto;
        width: 70%;
      }
      button {
        display: block;
        margin: 20px auto;
        padding: 10px 20px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s;
      }
      button:hover {
        background-color: #3e8e41;
      }
      form {
        display: block;
        margin: 20px auto;
        width: 70%;
        text-align: center;
      }
      input[type="file"] {
        display: inline-block;
        margin-right: 10px;
      }
      input[type="submit"] {
        display: inline-block;
        margin-left: 10px;
        padding: 10px 20px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s;
      }
      input[type="submit"]:hover {
        background-color: #3e8e41;
      }
iframe {
  width: 70%;
  height: 200px;
  border: 2px solid #ccc;
  border-radius: 5px;
  box-shadow: 0px 0px 5px #ccc;
  margin: 20px auto;
  display: block;
}
.button-group {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.button-group button {
  margin: 0 10px;
}
.credits {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #b4b4b4;
  color: white;
  font-size: 12px;
  height: 30px;
  line-height: 30px;
  text-align: right;
}

.credits a {
  color: white;
  text-decoration: none;
  margin-left: 10px;
}

.credits a:first-child {
  margin-left: 0;
} 





.dropdown-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

label {
  margin-right: 10px;
}

select {
  padding: 10px;
  font-size: 16px;
  border-radius: 4px;
  border: 1px solid #ccc;
  margin-right: 10px;
  width: 200px;
}

button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #3e8e41;
}








 </style>
  </head>
  <body>
    <h1>Kindlefusion</h1>
    <iframe name="myFrame" id="myFrame" src=""></iframe>
    <label for="myInput">Enter text to search:</label>
    <textarea id="myInput"></textarea>
<div class="button-group">
  <button onclick="sendToServer()">Check with StableHorde</button>
  <button onclick="unsplash()">Check with unsplash</button>
  <button onclick="unsplash_featured()">Random unsplash featured</button>
</div>

    <hr>
<BR>
    <h2>Image Upload </h2>
    <form method="post" action="/uploadthen" enctype="multipart/form-data" target="myFrame">
      <div>
        <input type="file" name="image">
        <input type="submit" value="Upload">
      </div>
    </form>


<BR><HR><BR><h2>Past images </h2>
<div class="button-group">
<select id="mySelect" name="options">
  <option value="Update options please">Option 1</option>
  <!-- add more options as needed -->
</select>

<button onclick="updateOptions()">Update</button>
<button onclick="showGallery()">Gallery</button>
<button onclick="loadOptions()">Load</button>




</div>


<div id="galleryPopup" style="display: none; position: fixed; top: 10%; left: 10%; width: 80%; height: 80%; background-color: white; border: 2px solid gray; border-radius: 10px; z-index: 9999; padding: 20px; overflow-y: scroll;">
  <h3>Gallery</h3>
  <div id="galleryThumbnails"></div>
  <button onclick="closeGallery()">Close</button>
</div>

<div class="credits">

  <span> </span>
<a href="#">| By Superpomme  </a>
  <a href="#">| Images provided by <a href="https://unsplash.com/">Unsplash</a> </a>
  <a href="#">| Image generation by <a href="https://stablehorde.net/">Stablehorde </a></a>
  <a href="#">| db0 - AI-Horde <a href="https://github.com/db0/AI-Horde">Github </a></a>

  <a href="#">| Many thanks to NiLuJe for tools and fbink <a href="https://github.com/NiLuJe/FBInk">Github</a> </a>

/

</div>



    <script>
      function sendToServer() {
        var frame = document.getElementById("myFrame");
        var input = document.getElementById("myInput").value;
        var url = "/do_html_fusion/" + input;
        frame.src = url;
      }
      function unsplash() {
        var frame = document.getElementById("myFrame");
        var input = document.getElementById("myInput").value;
        var url = "/image-search/" + input;
        frame.src = url;
      }
      function unsplash_featured() {
        var frame = document.getElementById("myFrame");

        var url = "/featured/";
        frame.src = url;
      }

function updateOptions() {
  fetch('/options/') // replace with your Flask endpoint
    .then(response => response.json())
    .then(data => {
      const select = document.getElementById('mySelect');
      select.innerHTML = '';
      data.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option.id;
        optionElement.text = `${option.id} | ${option.origin} | ${option.search_term}`;
        select.appendChild(optionElement);
      });
    });
}


function loadOptions() {
  const select = document.getElementById('mySelect');
  const selectedOption = select.options[select.selectedIndex].value;
  const url = `open_id/${selectedOption}`;
  document.getElementById('myFrame').src = url;
}

updateOptions()


function showGallery() {
  const select = document.getElementById('mySelect');
  const dropdownLength = select.length;

  const galleryContent = document.createElement('div');

const closeButton2 = document.createElement('button');
closeButton2.textContent = 'Close';
closeButton2.addEventListener('click', closeGallery);

galleryContent.appendChild(closeButton2);



  galleryContent.classList.add('popup-content');



  for (let i = 0; i < dropdownLength; i++) {
    const thumbnailContainer = document.createElement('div');
    thumbnailContainer.classList.add('thumbnail-container');
thumbnailContainer.classList.add('thumbnail-container');
thumbnailContainer.style.display = 'flex';
thumbnailContainer.style.alignItems = 'center';
thumbnailContainer.style.justifyContent = 'center';





    const thumbnail = document.createElement('img');
    thumbnail.src = `static/${select.options[i].value}.jpg`;
    thumbnail.style.width = "300px";
    thumbnail.style.border = "2px solid black";
    thumbnail.style.borderRadius = "10px";
    thumbnail.style.margin = "10px";

    const thumbnailLabel = document.createElement('span');
    thumbnailLabel.style.fontSize = "20px";
    thumbnailLabel.textContent = select.options[i].text;
    thumbnailLabel.style.marginRight = "10px";

    const button = document.createElement('button');
    button.textContent = 'Set';
    button.style.fontSize = "20px";
    button.onclick = () => {
      const id = select.options[i].value;
      const url = `open_id/${id}`;
      document.getElementById('myFrame').src = url;
    };

    thumbnailContainer.appendChild(thumbnail);
    thumbnailContainer.appendChild(thumbnailLabel);
    thumbnailContainer.appendChild(button);

    galleryContent.appendChild(thumbnailContainer);
  }

  const galleryPopup = document.getElementById('galleryPopup');
  galleryPopup.innerHTML = '';
  galleryPopup.appendChild(galleryContent);
  galleryPopup.style.display = 'block';

const closeButton = document.createElement('button');
closeButton.textContent = 'Close';
closeButton.addEventListener('click', closeGallery);

galleryContent.appendChild(closeButton);


}


  function closeGallery() {
    const galleryPopup = document.getElementById('galleryPopup');
    galleryPopup.style.display = 'none';
  }





    </script>











  </body>
</html>
 
''')


@app.route("/robprogress/<progressTime>")
def robprogress(progressTime):
    im = Image.new("RGBA", (600, 800),(0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    progressTime = int(progressTime)

    draw.rounded_rectangle((100, 375, 500, 450), fill='white',outline="black",  width=3, radius=17)

    fbfd = FBInk.fbink_open()
    FBInk.fbink_init(fbfd, fbink_cfg)
    draw = ImageDraw.Draw(im)

    display_fb(im)

    for i in range(progressTime):
        print ("waited {} seconds".format(i))
        printout="Loading {}/{} seconds".format(i,progressTime)
        FBInk.fbink_print(fbfd, printout.encode('ASCII'), fbink_cfg)
        time.sleep(1)

    FBInk.fbink_close(fbfd)
    return("should have worked")


def displayloading():
    im = Image.new("RGBA", (600, 800),(0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    

    draw.rounded_rectangle((100, 375, 500, 450), fill='white',outline="black",  width=3, radius=17)

    fbfd = FBInk.fbink_open()
    FBInk.fbink_init(fbfd, fbink_cfg)
    draw = ImageDraw.Draw(im)

    display_fb(im)


    
    FBInk.fbink_print(fbfd, "Loading...".encode('ASCII'), fbink_cfg)
   

    FBInk.fbink_close(fbfd)
    return("should have worked")




#upload and then set the kindle screen
@app.route('/uploadthen', methods=['POST'])
def uploadthen():
    file = request.files['image']
    im = Image.open(file.stream)

    # Rotate image if necessary
    if im.width > im.height:
        im = im.transpose(Image.ROTATE_270)

    # Resize image
    #im.thumbnail((600, 800), Image.ANTIALIAS)


    # Resize image
    #im.thumbnail((600, 800), Image.ANTIALIAS)

    width, height = im.size
    new_width = 600
    new_height = int(height * (new_width / width))
    im = im.resize((new_width, new_height), Image.ANTIALIAS)


    # Draw on image
    ImageDraw.Draw(im)
    # ...

    save_image(im ,"uploaded","unlisted name")

    # Display image
    display_fb(im)

    return "Image uploaded successfully!"




save_images=True







@app.route('/do_html_fusion/<text>')
def do_html_fusion(text):
            print("do fusion!")  
            displayloading()
            dofusion(text )
            return("I drew: {}".format(text) )



def display_fb(im ):

    # Now, make sure we'll pass raw data in a format FBInk/stb knows how to handle, doing as few conversions as possible.
    # If image is paletted, translate that to actual values, because stb won't know how to deal with paletted raw data...
    if im.mode == "P":
        print("Image is paletted, translating to actual values")
        # NOTE: No mode means "just honor the palette". Usually, that's RGB.
        #       We could also enforce Grayscale (L), but FBInk/stb will take care of that if needed.
        im = im.convert()

    # If image is not grayscale, RGB or RGBA (f.g., might be a CMYK JPEG) convert that to RGBA.
    if im.mode not in ["L", "RGB", "RGBA"]:
        print("Image data is packed in an unsupported mode, converting to RGBA")
        im = im.convert("RGBA")

    # And finally, get that image data as raw packed pixels.
    raw_data = im.tobytes("raw")

    raw_len = len(raw_data)
    print("Raw data buffer length: {}".format(raw_len))

    # Print the image using FBInk
    fbfd = FBInk.fbink_open()
    try:
        FBInk.fbink_init(fbfd, fbink_cfg)
        FBInk.fbink_print_raw_data(fbfd, raw_data, im.width, im.height, raw_len, 0, 0, fbink_cfg)
    finally:
        FBInk.fbink_close(fbfd)
    
is_loading=True
prev_log=""
def record_loop():
  while True:
    global prev_log
    global is_loading
    print("loop")
    with open(log_file, "r") as f:
        new_log = f.read()  # read the entire file

    if new_log != prev_log:
        print("i saw a difference!")
        # split the log file into sections based on the separator
        sections = new_log.split("==========\n")
        last_section = sections[-2].strip()  # -2 to skip the final empty section
        last_line = last_section.split('\n')[-1]  # get the last line of the last section
        print(last_line)
    
        # Get the text to send from the request
        text = last_line.encode('utf-8')
    
        # Send the text to the endpoint
        #url = 'http://{}:5000/text'.format(stable_ip)
        #response = requests.post(url, data=text)

        if is_loading==False:
            print("do fusion!")  
            displayloading()
            dofusion(text )
        else:
            print("loading")
            is_loading=False  

        # Return the response from the endpoint
        print ("printed {}".format(text))

        print("lengths are {} for old, {} for new".format(len(prev_log),len(new_log)))
       
        # update the previous log contents to the current contents
        prev_log=new_log

    time.sleep(1)  # wait for a second before checking the file again





def dofusion(searchterm):
    print("I was run")
    global horde_api_key
    class RequestData(object):
        def __init__(self):
                self.client_agent = "cli_request.py:1.1.0:(discord)db0#1625"
                self.api_key = horde_api_key

                self.filename = "test2.png"
                self.imgen_params = {
                    "n": 1,
                    "width": 384,
                    "height":512,
                    "steps": 50,
                    "sampler_name": "k_euler",
                    "cfg_scale": 7.5,
                    "denoising_strength": 0.6,
                }
                self.submit_dict = {
                    "prompt":searchterm,
                    "api_key": horde_api_key,
                    "nsfw": False,
                    "censor_nsfw": False,
                    "trusted_workers": False,
                    "models": ["stable_diffusion"],
                    "r2": True
                }
                self.source_image = None
                self.source_processing = "img2img"
                self.source_mask = None

        def get_submit_dict(self):
            submit_dict = self.submit_dict.copy()
            submit_dict["params"] = self.imgen_params
            submit_dict["source_processing"] = self.source_processing
            if self.source_image: 
                final_src_img = Image.open(self.source_image)
                buffer = BytesIO()
                # We send as WebP to avoid using all the horde bandwidth
                print("a webp bit")
                final_src_img.save(buffer, format="Webp", quality=95, exact=True)
                submit_dict["source_image"] = base64.b64encode(buffer.getvalue()).decode("utf8")
            if self.source_mask: 
                final_src_mask = Image.open(self.source_mask)
                buffer = BytesIO()
                # We send as WebP to avoid using all the horde bandwidth
                print("a webp bit2")
                final_src_mask.save(buffer, format="Webp", quality=95, exact=True)
                submit_dict["source_mask"] = base64.b64encode(buffer.getvalue()).decode("utf8")
            return(submit_dict)
        
    def load_request_data():
        request_data = RequestData()
        try:
            import cliRequestsData as crd
            try:
                request_data.api_key = crd.api_key
            except AttributeError:
                pass
            try:
                request_data.filename = crd.filename
            except AttributeError:
                pass
            try:
                for p in crd.imgen_params:
                    request_data.imgen_params[p] = crd.imgen_params[p]
            except AttributeError:
                pass
            try:
                for s in crd.submit_dict:
                    request_data.submit_dict[s] = crd.submit_dict[s]
            except AttributeError:
                pass
            try:
                request_data.source_image = crd.source_image
            except AttributeError:
                pass
            try:
                request_data.source_processing = crd.source_processing
            except AttributeError:
                pass
            try:
                request_data.source_mask = crd.source_mask
            except AttributeError:
                pass
        except:
            logger.warning("cliRequestData.py could not be loaded. Using defaults with anonymous account")
        if args.api_key: request_data.api_key = args.api_key 
        if args.filename: request_data.filename = args.filename 
        if args.amount: request_data.imgen_params["n"] = args.amount 
        if args.width: request_data.imgen_params["width"] = args.width 
        if args.height: request_data.imgen_params["height"] = args.height 
        if args.steps: request_data.imgen_params["steps"] = args.steps 
        if args.prompt: request_data.submit_dict["prompt"] = args.prompt 
        if args.nsfw: request_data.submit_dict["nsfw"] = args.nsfw 
        if args.censor_nsfw: request_data.submit_dict["censor_nsfw"] = args.censor_nsfw 
        if args.trusted_workers: request_data.submit_dict["trusted_workers"] = args.trusted_workers 
        if args.source_image: self.source_image = args.source_image
        if args.source_processing: self.source_processing = args.source_processing
        if args.source_mask: self.source_mask = args.source_mask
        return(request_data)


    @logger.catch(reraise=True)
    def generate():
        print("generateran")
        request_data = load_request_data()
        # final_submit_dict["source_image"] = 'Test'
        headers = {
            "apikey": request_data.api_key,
            "Client-Agent": request_data.client_agent,
        }
        # logger.debug(request_data.get_submit_dict())
        submit_req = requests.post(f'{args.horde}/api/v2/generate/async', json = request_data.get_submit_dict(), headers = headers)
        if submit_req.ok:
            submit_results = submit_req.json()
            logger.debug(submit_results)
            req_id = submit_results['id']
            is_done = False
            retry = 0
            cancelled = False
            try:
                while not is_done:
                    try:
                        chk_req = requests.get(f'{args.horde}/api/v2/generate/check/{req_id}')
                        if not chk_req.ok:
                            logger.error(chk_req.text)
                            return
                        chk_results = chk_req.json()
                        logger.info(chk_results)
                        is_done = chk_results['done']
                        time.sleep(0.8)
                    except ConnectionError as e:
                        retry += 1
                        logger.error(f"Error {e} when retrieving status. Retry {retry}/10")
                        if retry < 10:
                            time.sleep(1)
                            continue
                        raise
            except KeyboardInterrupt:
                logger.info(f"Cancelling {req_id}...")
                cancelled = True
                retrieve_req = requests.delete(f'{args.horde}/api/v2/generate/status/{req_id}')
            if not cancelled:
                retrieve_req = requests.get(f'{args.horde}/api/v2/generate/status/{req_id}')
            if not retrieve_req.ok:
                logger.error(retrieve_req.text)
                return
            results_json = retrieve_req.json()
            # logger.debug(results_json)
            if results_json['faulted']:
                final_submit_dict = request_data.get_submit_dict()
                if "source_image" in final_submit_dict:
                    final_submit_dict["source_image"] = f"img2img request with size: {len(final_submit_dict['source_image'])}"
                logger.error(f"Something went wrong when generating the request. Please contact the horde administrator with your request details: {final_submit_dict}")
                return
            results = results_json['generations']
            for iter in range(len(results)):
                final_filename = request_data.filename
                if len(results) > 1:
                    final_filename = f"{iter}_{request_data.filename}"
                if request_data.get_submit_dict()["r2"]:
                    logger.debug(f"Downloading '{results[iter]['id']}' from {results[iter]['img']}")
                    try:
                        img_data = requests.get(results[iter]["img"]).content
                    except:
                        logger.error("Received b64 again")


    




                    convert_and_show2(img_data,searchterm)








                else:
                    b64img = results[iter]["img"]
                    base64_bytes = b64img.encode('utf-8')
                    img_bytes = base64.b64decode(base64_bytes)
                    img = Image.open(BytesIO(img_bytes))
                    print("a png bit")
                    img.save("test.jpg" , format="JPG")
                    #img.save(final_filename , format="PNG")

                censored = ''
                if results[iter]["censored"]:
                    censored = " (censored)"
                logger.info(f"Saved{censored} {final_filename}")
        else:
            logger.error(submit_req.text)

    set_logger_verbosity(args.verbosity)
    quiesce_logger(args.quiet)

    try:
        import cliRequestsData as crd
        logger.info("Imported cliRequestsData")
    except:
        logger.warning("No cliRequestsData found, use default where no CLI args are set")
        class temp(object):
            def __init__(self):
                self.filename = "test2.png"
                self.imgen_params = {
                    "n": 1,
                    "width": 384,
                    "height":512,
                    "steps": 50,
                }
                self.submit_dict = {
                    "prompt": "A donkey with wings",
                    "api_key": horde_api_key,
                }
        crd = temp()







    generate()
    #convert_and_show()






def convert_and_show2(incoming_image,searchterm):

    # Set up HTTP basic authentication credentials
    global converter_auth
    auth = converter_auth

    # Open the file in binary mode
    
    # Send a POST request to the Flask endpoint with the image file in the payload
    response = requests.post('http://192.168.0.2:5000/resize_image', files={'image': ("test2.png",incoming_image)}, auth=auth)
      
    im = Image.open(BytesIO(response.content))
    draw = ImageDraw.Draw(im)

    display_fb(im )
  

    if isinstance(searchterm, bytes):
        searchterm = searchterm.decode('utf-8')

    if save_images==True:
        save_image(im,"stablehorde",searchterm)




import pickle 



def check_gallery_count():
    loaded_dict_array = load_dict_array()
    return(len(loaded_dict_array))

def load_dict_array():

    try:
        with open('gallery/gallery.txt', 'rb') as f:
            loaded_dict_array = pickle.load(f)
    except:
        loaded_dict_array = []
    return loaded_dict_array


    
def save_dict(current_dict_array):
    with open('gallery/gallery.txt', 'wb') as f:
        pickle.dump(current_dict_array, f)

def update_gallery(the_id, the_name,origin_location): #4,"a donkey",stable
    pass






@app.route('/options/')
def get_options():
    options = load_dict_array()
    print(options )
    return jsonify(options)








def save_image(img_data,image_origin,search_term):

    current_dict_array=load_dict_array()
    current_id_array=len(current_dict_array)



    #if image_origin=="stablehorde":
    #    with open("gallery/images/{}.jpg".format(current_id_array), 'wb') as handler:
    #        print("the handler is saving")
    #        handler.write(img_data)
    #else:
    img_data.save('gallery/images/{}.jpg'.format(current_id_array))



    current_dict_array.append({"id": current_id_array, "origin": image_origin, "search_term": search_term})

    print(current_dict_array)
    save_dict(current_dict_array) 

# Define the API endpoint
api_endpoint = 'https://source.unsplash.com/featured/?'

# Define a route to handle the search query
@app.route('/image-search/<query>')
def search_images(query):
    displayloading()
    # Set up the API request parameters
    url = api_endpoint + query
    
    # Send the API request and get the response
    response = requests.get(url)
    
    # Download and return the image
    im = Image.open(BytesIO(response.content))


    # Rotate image if necessary
    if im.width > im.height:
        im = im.transpose(Image.ROTATE_270)

    # Resize image

    width, height = im.size
    new_width = 600
    new_height = int(height * (new_width / width))
    im = im.resize((new_width, new_height), Image.ANTIALIAS)


    # Draw on image
    draw = ImageDraw.Draw(im)




    display_fb(im )

    save_image(im ,"unsplash",query)

    return("done")


# Define a route to handle the search query
@app.route('/featured/')
def featured():
    displayloading()
    # Set up the API request parameters
    url = "https://source.unsplash.com/featured/"
    
    # Send the API request and get the response
    response = requests.get(url)
    
    # Download and return the image
    im = Image.open(BytesIO(response.content))


    # Rotate image if necessary
    if im.width > im.height:
        im = im.transpose(Image.ROTATE_270)

    # Resize image
    #im.thumbnail((600, 800), Image.ANTIALIAS)

    width, height = im.size
    new_width = 600
    new_height = int(height * (new_width / width))
    im = im.resize((new_width, new_height), Image.ANTIALIAS)

    # Draw on image
    draw = ImageDraw.Draw(im)

    display_fb(im )
    save_image(im ,"unsplash featured","random")
    return("done")


@app.route('/open_id/<id_to_open>')
def open_from_id(id_to_open):
    open_image = Image.open("gallery/images/{}.jpg".format(id_to_open))
    display_fb(open_image)
    return "image {} applied".format(id_to_open)

if __name__ == "__main__":
   #recording_on = Value('b', True)
   #p = Process(target=record_loop, args=(recording_on,))
   p = Process(target=record_loop)
   p.start()  
   app.run(debug=False,host='0.0.0.0')
   p.join()
   




 
