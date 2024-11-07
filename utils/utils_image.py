from PIL import Image
import time
import io
import base64
import random
import string
import mimetypes

def generate_image_name(extension="png"):
    # Get the current timestamp
    timestamp = int(time.time())
    
    # Generate a random string of 6 characters
    random_str = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=6))
    
    # Combine timestamp and random string to create the image name
    image_name = f"image_{timestamp}_{random_str}.{extension}"
    
    return image_name

def convert_base64_to_bytesIO(image_base64):
    image_bytes = base64.b64decode(image_base64)
    image_buffer = io.BytesIO(image_bytes)

    return image_buffer

def convert_pil_to_base64(image: Image.Image, format: str = 'JPEG') -> str:
    if image.mode == 'RGBA':
        image = image.convert('RGB')
        
    with io.BytesIO() as buffer:
        image.save(buffer, format=format)
        image_bytes = buffer.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    return image_base64

def image_base64_to_buffer(image_base64):
    image_buffer = convert_base64_to_bytesIO(image_base64)
    image = Image.open(image_buffer)

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    return img_byte_arr


def get_mime_type(filename):
    mime_type, encoding = mimetypes.guess_type(filename)
    return mime_type