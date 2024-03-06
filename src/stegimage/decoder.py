import numpy as np
from PIL import Image

from helper import is_encoded_pixel, get_encrypted_bit, bin2str

def decode_text(img_path: str, key: int) -> str:
    """
    Decodes image for encrypted text.
    """

    img = Image.open(img_path).convert("RGB")
    length, height = img.getbbox()[2]-img.getbbox()[0], img.getbbox()[3]-img.getbbox()[1]
    curr = (0, 0)

    lsb_list = []

    for x in range(key*8):
        pxl = img.getpixel(curr)
        lsb_list += [get_encrypted_bit(pxl)]

        curr = (curr[0]+1, curr[1])

        if (curr[0] == length):
            curr = (curr[0], curr[1]+1)

    return bin2str(lsb_list)

def decode_stencil(img_path: str, key: int) -> Image.Image:
    """
    Decodes image for encrypted stencil.
    """

    img = Image.open(img_path).convert("RGB")

    length, height = img.getbbox()[2]-img.getbbox()[0], img.getbbox()[3]-img.getbbox()[1]

    for y in range(height):
        for x in range(length):
            if (is_encoded_pixel(img.getpixel((x, y)), key)):
                # sets decrypted pixels to green
                img.putpixel((x, y), (0, 255, 0))

    return img