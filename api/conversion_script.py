from flask import Flask, request, send_file, abort
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
from PIL import Image
import io

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day", "50 per hour","1 per 10 second"],
    storage_uri="memory://",
)
auth = HTTPBasicAuth()

# Set maximum file size in bytes
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Set allowed file extensions
ALLOWED_EXTENSIONS = {'png'}

def allowed_file(filename):
    """
    Check if the file has an allowed extension
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_input_data(data):
    """
    Validate input data to ensure that it conforms to expected formats and values
    """
    # Check if the data contains the 'image' key
    if 'image' not in data:
        abort(400, 'No image found in request')

    # Get the uploaded file
    uploaded_file = data['image']

    # Validate file size
    if len(uploaded_file.read()) > MAX_FILE_SIZE:
        abort(400, 'File size is too large')

    # Reset file pointer to the beginning of the file
    uploaded_file.seek(0)

    # Validate file extension
    if not allowed_file(uploaded_file.filename):
        abort(400, 'File type is not supported')

    # Sanitize filename
    filename = secure_filename(uploaded_file.filename)

    # Open the image with PIL
    try:
        pil_image = Image.open(io.BytesIO(uploaded_file.read()))
    except:
        abort(400, 'Invalid image file')

    # Resize the image
    resized_image = pil_image.resize((600, 800))

    img_io = io.BytesIO()
    resized_image.save(img_io, format="JPEG")
    img_io.seek(0)

    return img_io
    
#@limiter.exempt
@auth.verify_password
def verify_password(username, password):
    if username == 'stablehorde' and password == 'sdf676_83g!!!das':
        return True
    return False
    

@app.route('/resize_image', methods=['POST'])
@auth.login_required
def resize_image():
    # Validate input data
    img_io = validate_input_data(request.files)

    # Return resized image as response
    return send_file(img_io, mimetype='image/jpg')



if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
