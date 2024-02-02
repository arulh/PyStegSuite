from PIL import Image, ImageDraw, ImageFont
import numpy as np

from helper import encode_pixel, generate_key

def encode_stencil(img_path: str, encoded_text: str, text_size=75, text_coords=(50, 50)) -> np.array:
    """
    Encodes the text into the image using a stencil approach.
    """
    
    img = Image.open(img_path).convert("RGBA")
    img_data = np.array(img)

    fnt = ImageFont.load_default(text_size)
    text_length = int(fnt.getlength(encoded_text))

    text_img = Image.new("RGB", (text_length, text_size), color="white")
    
    draw = ImageDraw.Draw(text_img)
    
    draw.text((0, 0), text=encoded_text, fill=(0, 255, 0), font=fnt)

    key = generate_key()

    for y in range(text_size):
        for x in range(text_length):
            if (text_img.getpixel((x, y)) == (0, 255, 0)):
                img_data[y][x] = encode_pixel(img_data[y][x], key)

    return img_data