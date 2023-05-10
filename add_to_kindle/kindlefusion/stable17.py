# Kindlefusion
version="17c"

import json
with open('/mnt/us/kindlefusion/secret_config.json') as f:
    secret_config = json.load(f)
#print(secret_config)

#Note that you can do it without this, but it defaults to a slower response
horde_api_key = secret_config['horde_api_key']
#horde_api_key = secret_config['horde_api_key']
loaded_kindlename = secret_config['kindlename']
#auth for the webp converter
converter_auth = tuple(secret_config['converter_auth'])


import socket

import requests,  os, time, argparse, base64
from cli_logger import logger, set_logger_verbosity, quiesce_logger, test_logger
from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageOps,PngImagePlugin
from io import BytesIO
from requests.exceptions import ConnectionError
from flask import Flask,request,jsonify,send_file, render_template
from flask_cors import CORS, cross_origin
import os
from datetime import datetime
import io
kindle_highlights = True #this should be False but you are lazily stopping it until you have the menui


#this section can likely be removed, I haven't tested. This came from the stable horde library
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-n', '--amount', action="store", required=False, type=int, help="The amount of images to generate with this prompt")
arg_parser.add_argument('-p','--prompt', action="store", required=False, type=str, help="The prompt with which to generate images")
arg_parser.add_argument('-w', '--width', action="store", required=False, type=int, help="The width of the image to generate. Has to be a multiple of 64")
arg_parser.add_argument('-l', '--height', action="store", required=False, type=int, help="The height of the image to generate. Has to be a multiple of 64")
arg_parser.add_argument('-s', '--steps', action="store", required=False, type=int, help="The amount of steps to use for this generation")
arg_parser.add_argument('--api_key', type=str, action='store', required=False, help="The API Key to use to authenticate on the Horde. Get one in https://stablehorde.net")
arg_parser.add_argument('-f', '--filename', type=str, action='store', required=False, help="The filename to use to save the images. If more than 1 image is generated, the number of generation will be prepended")
arg_parser.add_argument('-v', '--verbosity', action='count', default=5, help="The default logging level is ERROR or higher. This value increases the amount of logging seen in your screen")
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
app.static_folder = 'gallery/'
app.static_url_path = '/static'
cors = CORS(app)
#import requests

# Load Pillow
#from PIL import Image, ImageDraw, ImageFont
import random
from random import randint

# Load the FBInk wrapper module
from _fbink import ffi, lib as FBInk

from io import BytesIO


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



@app.route("/caaam")
def caaam():
    file_path = '/mnt/us/kindlefusion/gallery/caaam_mini.html'
    return send_file(file_path, as_attachment=False)


@app.route("/uploader")
def uploader():
    render_template('uploader.html')



@app.route("/")
def thehome():
      return render_template('welcome.html' ,loaded_kindlename=loaded_kindlename,version=version)

@app.route("/sethordeapikey/<apikey>")
def sethordeapikey(apikey):
    global horde_api_key
    if apikey != "" and apikey != "{{ loaded_kindlename }}":
        horde_api_key=apikey
        
        
        with open('secret_config.json') as f:
            secret_config = json.load(f)

        # Modify the value of "horde_api_key"
        secret_config["horde_api_key"] = horde_api_key

        # Save the updated JSON data back to the file
        with open('secret_config.json', 'w') as f:
            json.dump(secret_config, f)
                
                
        
        
        return ("api key set")
    
    else:
        return("you left this blank")
    
    
@app.route("/setname/<name_to_set>")
def setname(name_to_set):
    global loaded_kindlename
    if (name_to_set!=""):
        loaded_kindlename=name_to_set
        
        
        with open('secret_config.json') as f:
            secret_config = json.load(f)

        # Modify the value of "horde_api_key"
        secret_config["kindlename"] = loaded_kindlename

        # Save the updated JSON data back to the file
        with open('secret_config.json', 'w') as f:
            json.dump(secret_config, f)
                
                
        
        
        return ("name changed")
    
    else:
        return("you left this blank")
    
    



# Enabling and disabling screensaver
@app.route("/enablescreensaver")
def enablescreensaver():
    cmd = 'lipc-set-prop -i com.lab126.powerd preventScreenSaver 0'
    result = os.popen(cmd).read()
    return "Screensaver Enabled"
@app.route("/disablescreensaver")
def disablescreensaver():
    cmd = 'lipc-set-prop -i com.lab126.powerd preventScreenSaver 1'
    result = os.popen(cmd).read()
    return "Screensaver Disabled"




@app.route("/home")
def home(theheight=285):
    theheight=int(theheight)
    randnum=random.randint(184,193)
    im = Image.open("./static/alien({}).png".format(randnum))

    # Create a new image with the same dimensions as the original
    new_im = Image.new(im.mode, (800,1000))
    



    orig_pixel_map = im .load()
    first_pixel = orig_pixel_map [0, 0]
    print(f"\nFirst pixel: {first_pixel}")



   

    # Determine image size
    image_width = 600
    image_height = 800

    # Create image

    draw = ImageDraw.Draw(new_im)

    shadow_coords = (0, 0, 600, 800)
    draw.rectangle(shadow_coords, fill=first_pixel)


    # Paste the original image onto the new image at the desired coordinates
    new_im.paste(im, (50, theheight))


    bar_height=75
    page_num="page1"

    # Draw page number
    page_num_box = (0, 0, image_width, bar_height)
    draw.rectangle(page_num_box, fill=(0, 0, 0))
    #page_num_text = f"Page {page_num}"
    page_num_text = f"Version {version}"


    ipaddr=getip()

    global loaded_kindlename
   

    # Specify the font and text to be drawn
    caption = loaded_kindlename
    font = ImageFont.truetype("/usr/java/lib/fonts/KindleBlackboxBoldItalic.ttf", 120)
    
    # Get the size of the text
    text_width, text_height = draw.textsize(caption, font=font)
    
    # Calculate the coordinates for the center of the image
    image_width, image_height = im.size
    x = (image_width - text_width) / 2
    #y = (image_height - text_height) / 2
    y=130
    
    # Draw the text
    draw.text((x+50, y), caption, fill='black', font=font, stroke_width=5, stroke_fill='white')

   
    draw.text((150, 50), page_num_text, fill=(255, 255, 255), font=ImageFont.truetype("/mnt/base-us/extensions/MRInstaller/data/BigBlue_Terminal.ttf", 20), anchor="mm")
    draw.text((450, 50), "{}:5000".format(ipaddr), fill=(255, 255, 255), font=ImageFont.truetype("/mnt/base-us/extensions/MRInstaller/data/BigBlue_Terminal.ttf", 20), anchor="mm")
    
    display_fb(new_im)
    return "Ok!"





def getip(interface="wlan0"):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except:
            ip = ''
    return ip




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



@app.route('/do_html_fusion_js/<text>')
@cross_origin()
@cross_origin()
def do_html_fusion_js(text):
            print("d------------------------------------------------------------")  
            print("do fusion js!")  
            displayloading()
            img_data=dofusion(text ,"jsconvert")
            
            

            #print("img_data")  
            #print("some image data")  

            
            with open('./temp2.png', 'rb') as gee:
                encoded = base64.b64encode(gee.read()).decode('utf-8')



            return(encoded)


            print("----------------------")
            print(encoded)
            print("----------------------")
            return(encoded)          
            



@app.route('/do_html_fusion/<text>')
def do_html_fusion(text):
            print("d-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx----------------------------------------------------") 
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
    print("record loop")
    global kindle_highlights
    while kindle_highlights:
        global prev_log
        global is_loading
        print("loop", flush=True)
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

        time.sleep(5)  # wait for a second before checking the file again


@app.route('/download_caaam')
def download_caaam():
    file_path = '/mnt/us/kindlefusion/gallery/caaam9.html'
    return send_file(file_path, as_attachment=True)

@app.route('/download_caaam_image')
def download_caaam_image():
    file_path = '/mnt/us/kindlefusion/gallery/camera.png'
    return send_file(file_path, as_attachment=True)
    
# robapi, jsconvert
def dofusion(searchterm,tag="robapi"):
    print("I was run with tag : {}".format(tag))
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



    # robapi, jsconvert

    @logger.catch(reraise=True)
    def generate(tag):
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
                        wait_time = chk_results['wait_time']
                        os.system(f"eips 35 20 '{wait_time}'")
                        
                        #os.system("eips 10 10 'hi'")
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
                        logger.error("Received b64 again------------------------------")


    



                    if tag=="jsconvert":
                    
                        print("JS SHOULD BE CONVERTING,JS SHOULD BE CONVERTING JS SHOULD BE CONVERTING")
                        with open("./temp2.png", 'wb') as handler:
                           handler.write(img_data)
                        
                        
                        return img_data
                    else:    
                        print("JS SHOULDNOT be converting")
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







    returnimage=generate(tag)
    return returnimage
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
        with open('/mnt/us/kindlefusion/gallery/new_gallery.txt', 'rb') as f:
            loaded_dict_array = pickle.load(f)
    except FileNotFoundError:
        loaded_dict_array = []
    return loaded_dict_array


def load_dict_array():
    logger.error("I am running load_dict_array")
    try:
        with open('/mnt/us/kindlefusion/gallery/new_gallery.txt', 'r') as f:
            # Check if file is empty
            if os.stat('/mnt/us/kindlefusion/gallery/new_gallery.txt').st_size == 0:
                loaded_dict_array = []
                logger.error("I am running blanking")
            else:
                logger.error("I am running floading")
                loaded_dict_array = json.load(f)
                #logger.error(loaded_dict_array)
                
    except FileNotFoundError:
        logger.error("I am running file not found")
        loaded_dict_array = []
    return loaded_dict_array



def save_dict(current_dict_array):
    with open('/mnt/us/kindlefusion/gallery/new_gallery.txt', 'w', encoding='utf-8') as f:
        json.dump(current_dict_array, f, ensure_ascii=False, indent=4)


@app.route('/options/')
def get_options():
    options = load_dict_array()
    #print(options )
    reversed_options = list(reversed(options))
    return jsonify(reversed_options)




def save_image(img_data,image_origin,search_term):
    logger.error(">>>>>>save_image<<<<<<<<<<<")

    current_dict_array=load_dict_array()
    #logger.error(current_dict_array)
    #print("current_dict_array")
    #print(current_dict_array)    
    
    #current_id_array=len(current_dict_array)
    # Generate a string with the current date and time
    now = datetime.now()
    timestamp = now.strftime('%d%m%Y_%H_%M_%S')

    # Save the image with the timestamp as the filename
    
    img_data.save('gallery/images/{}.jpg'.format(timestamp))
    current_dict_array.append({"id": timestamp, "origin": image_origin, "search_term": search_term})
    #logger.error(current_dict_array)
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



process_running = False




def start_process():
    print("started")
    global kindle_highlights
    if not kindle_highlights: # lazily stopped it from running. this will need correcting
        kindle_highlights = True
        p = Process(target=record_loop)
        p.start()
        #p.join()
        #html_fusion
    else:
        print("Kindle Highlights disabled")


def stop_process():
    global kindle_highlights
    if kindle_highlights:
        kindle_highlights = False





print("--------------------------------------------------------------launching kindlefusion {}".format(version))
home()



@app.route('/open_id/<id_to_open>')
def open_from_id(id_to_open):
    open_image = Image.open("/mnt/us/kindlefusion/gallery/images/{}.jpg".format(id_to_open))
    display_fb(open_image)
    return "image {} applied".format(id_to_open)



@app.route('/remove_id/<id_to_remove>')
def remove_id(id_to_remove):
    #open_image = Image.open("/mnt/us/kindlefusion/gallery/images/{}.jpg".format(id_to_open))
    #display_fb(open_image)
    
    

    logger.error("I am removing {}".format(id_to_remove))

    # Load the current dictionary array from the file
    current_dict_array = load_dict_array()

    # Define the incoming variable
    incoming_id = id_to_remove
    #print(current_dict_array)
    # Iterate over each dictionary in the array
    for dictionary in current_dict_array:
        # Check if the "id" key in the dictionary matches the incoming variable
        if dictionary["id"] == incoming_id:
            # Remove the dictionary from the array
            current_dict_array.remove(dictionary)
            break

    # Print the updated dictionary array
    #print(current_dict_array)
    save_dict(current_dict_array) 

    # Define the path to the file
    file_path = 'gallery/images/{}.jpg'.format(incoming_id)

    # Check if the file exists
    if os.path.exists(file_path):
        # Remove the file
        os.remove(file_path)
        print("File removed successfully")
    else:
        print("File does not exist")

    
    return "image {} removed".format(id_to_remove)


# the stuff from automatic bridge


@app.route('/text/<remote_address>/<text>', methods=['POST',"GET"])
def handle_text(text,remote_address):
    global lastrequest
    print("waiting for loading")

    displayloading()
    print("finished waiting for loading")    
    print(request.remote_addr)
    #text = request.get_data().decode('utf-8')
    
    #startcountdown()
    #t = threading.Thread(target=startcountdown)
    #t.start()    
    
    print("-----------------------")
    print("i sense incoming:    {}".format(text))
    print("-----------------------")
    
    #this is for a quick repeat of the last prompt
    #if text == "a":
    #    text=lastrequest
    #else:
    #    lastrequest=text
    lastrequest=text
        
    #text=text+". {}".format(book_details)    
    
    
    # Run the script on the text
    url = "http://{}:7860".format(remote_address)
    print("-------------------a--------------:")
    print("attempting:")
    print(url)
    payload = {
        "prompt": text,
        "steps": 20,
        "width":600,
        "height":800,
        "negative_prompt":"poorly drawn hands, poorly rendered hands, bad composition, mutated body parts, disfigured, bad anatomy, deformed body features, deformed hands,blurry"
    }
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    print("attempting2:")
    print(f'{url}/sdapi/v1/txt2img')    
    
    r = response.json()
    print("got the return from stablediff")
    #print(r)
    # Save the resulting image to a file
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        
        im = image

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
        save_image(im ,"Automatic1111",text)     
        print("should have saved")
        display_fb(im )
      
        
        
    return 'OK'






if __name__ == "__main__":
   start_process()
   
   app.run(debug=False,host='0.0.0.0')



 