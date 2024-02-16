import numpy as np
from PIL import Image

from helper import is_encoded_pixel

def decode_stencil(img_path: str, key: int) -> Image.Image:
    """
    Decodes image for encrypted stencil.
    """

    img = Image.open(img_path).convert("RGBA")

    length, height = img.getbbox()[2]-img.getbbox()[0], img.getbbox()[3]-img.getbbox()[1]

    for y in range(height):
        for x in range(length):
            if (is_encoded_pixel(img.getpixel((x, y)), key)):
                # sets decrypted pixels to green
                img.putpixel((x, y), (0, 255, 0))

    return img