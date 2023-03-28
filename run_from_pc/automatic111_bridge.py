#bridge to pass through requests from kindlefusion highlighting to local Automatic1111
# when this is set to API but not sharing across the lan. Adress for the kindle needs to be set, or it needs to
#get the kindle address from the request

import requests
import io
import base64
from flask import Flask, request
from PIL import Image, PngImagePlugin
import threading
app = Flask(__name__)


kindle_ip="192.168.15.244"
countdown_time=19 # You can poll the api but it always takes the same length for me anyway

#I'm hard setting this here for testing, but you can pull this same info from the other script    
#book_details="From the book 'Guards Guards' in the Discworld series written by Terry Pratchett"  
book_details=""

lastrequest=""


@app.route("/")
def thehome():
   
    return(''' 
<!DOCTYPE html>
<html>
  <head>
    <title>Send iframe to server</title>
  </head>
  <body>
    <iframe id="myFrame" src="https://www.example.com"></iframe>
    <br>
    <input type="textarea" id="myInput">
    <button onclick="sendToServer()">Send to server</button>

    <script>
      function sendToServer() {
        var frame = document.getElementById("myFrame");
        var input = document.getElementById("myInput").value;
        var url = "http://127.0.0.1:5000/test/" + input;
        frame.src = url;
      }
    </script>
  </body>
</html>''')

@app.route('/text', methods=['POST'])
def handle_text():
    global lastrequest
    print(request.remote_addr)
    text = request.get_data().decode('utf-8')
    
    #startcountdown()
    t = threading.Thread(target=startcountdown)
    t.start()    
    
    print("-----------------------")
    print("i sense incoming:    {}".format(text))
    print("-----------------------")
    
    #this is for a quick repeat of the last prompt
    if text == "a":
        text=lastrequest
    else:
        lastrequest=text
        
    text=text+". {}".format(book_details)    
    
    
    # Run the script on the text
    url = "http://127.0.0.1:7860"
    payload = {
        "prompt": text,
        "steps": 20,
        "width":600,
        "height":800,
        "negative_prompt":"poorly drawn hands, poorly rendered hands, bad composition, mutated body parts, disfigured, bad anatomy, deformed body features, deformed hands,blurry"
    }
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    r = response.json()
    print("got the return from stablediff")
    # Save the resulting image to a file
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        image.save('output.png', pnginfo=pnginfo)


        sendimagepng()
    return 'OK'
    
    
def startcountdown():
    trigger_countdown = requests.get('http://{}:5000/robprogress/20'.format(kindle_ip))
    print(trigger_countdown)
    return("done")
 

@app.route('/sendimagepng')
def sendimagepng():   

    url = 'http://{}:5000/uploadthen'.format(kindle_ip)

    # Open the image file and read its contents as bytes
    with open('output.png', 'rb') as f:
        image_data = f.read()

    # Send the image to the /upload endpoint as a file upload
    response = requests.post(url, files={'image': image_data})

    # Print the response from the server
    print(response.text)   


@app.route('/test/<input>')
def send_text(input):
    # Get the text to send from the request
    text = input

    # Send the text to the endpoint
    url = 'http://127.0.0.1:5000/text'
    response = requests.post(url, data=text)

    # Return the response from the endpoint
    return response.text

(1)


if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')


