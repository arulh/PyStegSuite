from PIL import Image, ImageDraw, ImageFont
import numpy as np

from helper import encode_pixel, generate_key

def encode_stencil(img_path: str, text: str, text_size=75, text_coords=(50, 50)) -> np.array:
    """
    Encodes the text into the image using a stencil approach.
    """

    print("encode_stencil")
    
    img = Image.open(img_path).convert("RGBA")
    img_data = np.asarray(img)

    text_img = Image.new("RGB", (500, 100), color="white")
    # fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", text_size)
    draw = ImageDraw.Draw(text_img)
    draw.text((0, 0), text, fill=(0, 255, 0))
    # text_img.show()

    key = generate_key()

    for y in range(100):
        for x in range(500):
            if (text_img.getpixel((x, y)) == (0, 255, 0)):
                img_data[y][x] = encode_pixel(img_data[y][x], key)

    return img_data