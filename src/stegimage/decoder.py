import numpy as np
from PIL import Image
from .encoder import Encoder

from .helper import is_encoded_pixel, get_encrypted_bit, bin2str

class Decoder:

    def __init__(self, type: str, img: Image.Image, key: int) -> None:
        if (type == "text"):
            res = self._decode_text(key, img=img)
            print(res)
        else:
            res = self._decode_stencil(key, img=img)
            res.show()

    def _decode_text(key: int, img_path: str=None, img: Image.Image=None) -> str:
        """
        Decodes image for encrypted text.
        """

        # checks if atleast one image argument is provided
        if (img_path == None and img == None):
            raise ValueError("MUST PROVIDE IMAGE ARGUMENT")
        
        if (img_path != None and img == None):
            img = Image.open(img_path).convert("RGB")
        else:
            # default to using img argument
            img = img.convert("RGB")

        length, height = img.getbbox()[2]-img.getbbox()[0], img.getbbox()[3]-img.getbbox()[1]
        curr = (0, 0)

        lsb_list = []

        for x in range(key*8):
            pxl = img.getpixel(curr)
            lsb_list += [get_encrypted_bit(pxl)]

            curr = (curr[0]+1, curr[1])

            if (curr[0] == length):
                curr = (0, curr[1]+1)

        return bin2str(lsb_list)

    def _decode_stencil(key: int, img_path: str=None, img: Image.Image=None) -> Image.Image:
        """
        Decodes image for encrypted stencil.
        """

        if (img_path == None and img == None):
            raise ValueError("MUST PROVIDE IMAGE ARGUMENT")
        
        if (img_path != None and img == None):
            img = Image.open(img_path).convert("RGB")
        else:
            # default to using img argument
            img = img.convert("RGB")

        length, height = img.getbbox()[2]-img.getbbox()[0], img.getbbox()[3]-img.getbbox()[1]

        for y in range(height):
            for x in range(length):
                if (is_encoded_pixel(img.getpixel((x, y)), key)):
                    # sets decrypted pixels to green
                    img.putpixel((x, y), (0, 255, 0))

        return img