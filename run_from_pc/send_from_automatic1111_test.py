
# You could either manually enter the folder, or use the date to work out which subfolder. 

import datetime

import requests
from PIL import Image
from io import BytesIO
import time

folder_address="C:/projects/stable/automatic/automatic3/stable-diffusion-webui/outputs/txt2img-images"
upload_path="http://192.168.15.244:5000/uploadthen"

upload_path_array=[
    #"http://192.168.0.229:5000/uploadthen",
    #"http://192.168.0.202:5000/uploadthen",
    #"http://192.168.0.202:5000/uploadthen",
    #"http://192.168.0.200:5000/uploadthen",
    "http://192.168.0.229:5000/uploadthen"
    #"http://192.168.0.219:5000/uploadthen",
   
]


def get_upload_path(upload_path_array):
    index = 0
    while True:
        yield upload_path_array[index]
        index = (index + 1) % len(upload_path_array)
        
uploader = get_upload_path(upload_path_array)


#upload_path = next(uploader)
#print(upload_path)  # "http://192.168.15.244:5000/uploadthen"
#
#upload_path = next(uploader)
#print(upload_path)  # "http://192.168.15.214:5000/uploadthen"
#
#upload_path = next(uploader)
#print(upload_path)  # "http://192.168.15.224:5000/uploadthen"
#
#upload_path = next(uploader)
#print(upload_path)  # "http://192.168.15.244:5000/uploadthen" (loops back to the beginning)

print("--------------------------------------------------------------------------")
print("--------------------------------------------------------------------------")
print("-------------------------Starting monitor---------------------------------")
print("--------------------------------------------------------------------------")
print("--------------------------------------------------------------------------")

#using most recent automatic1111 which places in subfolders sorted by day. Update this address

#print(folder_address)

#get the folder
current_date = datetime.date.today()
directory_date = current_date.strftime('%Y-%m-%d')

directory_path="{}\{}".format(folder_address,directory_date)

print("-------------")
print("monitoring {}".format(directory_path))
print("-------------")

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class NewFileHandler(FileSystemEventHandler):
    #def on_created(self, event):
    #    print(event)
    #    if event.is_directory:
    #        return None
    #    else:
    #        print(f"New file created: {event.src_path}")
    #
    #def on_modified(self, event):
    #    print(event.src_path, event.event_type)
    #
    #def on_any_event(self, event) :
    #    print("------------------")
    #    print(event.src_path, event.event_type)
    
    def on_moved(self, event):
        if event.is_directory:
            return
        print("***********")            
        src_path = event.src_path
        dst_path = event.dest_path
        #print(f"File moved: {src_path} to {dst_path}")  
        if (dst_path[-4:]==".png"):    
            print("File change detected")
            print(dst_path)
            send_off_image(dst_path)
    
#folder_path = "path/to/folder" # replace with your folder path
event_handler = NewFileHandler()
observer = Observer()
observer.schedule(event_handler, directory_path, recursive=False)
observer.start()


def send_off_image(dst_path):
    img = Image.open(dst_path)
    # Resize the image
    img_bytes=fix_filesize(img) 

    # Send the image to the endpoint as form data
    #url = upload_path
    
    url = next(uploader)
    files = {'image': ('output.png', img_bytes, 'image/png')}
    response = requests.post(url, files=files)

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("justsend {} to {}".format(dst_path,url))

    # Display the response from the endpoint
    print( response.text)


def fix_filesize(img):

    # Resize the image
    img.thumbnail((600, 800), Image.ANTIALIAS)

    # Convert the image to bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)  
    return (img_bytes)    





try:
    while True:
        #observer.join()
        time.sleep(1)
        pass
except KeyboardInterrupt:
    observer.stop()



