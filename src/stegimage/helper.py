from PIL import Image, ImageDraw, ImageFont
import random

def encode_pixel(pixel: tuple, key: int) -> tuple:
    """
    Encodes the key into the lower order bits of the pixels RGB values.

    Parameters:
    Returns: Encoded pixel as tuple.
    """

    key = key%64

    # extract RGB values from pixel
    r, g, b = pixel[0], pixel[1], pixel[2]

    # convert key to a binary string
    binary_key = bin(key)[2:].zfill(6)

    # encode the lower order bits of the RGB values with the key
    encoded_r = (r & 0b1111111100) | int(binary_key[0:2], 2)
    encoded_g = (g & 0b1111111100) | int(binary_key[2:4], 2)
    encoded_b = (b & 0b1111111100) | int(binary_key[4:6], 2)

    return (encoded_r, encoded_g, encoded_b)

def is_encoded_pixel(pixel: tuple, key: int) -> bool:
    """
    Parameters: pixel is from encoded image
    Returns: true if pixels is encoded using that key and false otherwise
    """

    key = key%64

    # convert key to a binary string
    binary_key = bin(key)[2:].zfill(6)

    # extract RGB values from potential encoded pixel
    r, g, b = pixel[0], pixel[1], pixel[2]

    r_bin = str(bin(r)[2:]).zfill(8)[6:]
    g_bin = str(bin(g)[2:]).zfill(8)[6:]
    b_bin = str(bin(b)[2:]).zfill(8)[6:]

    return binary_key[0:2] == r_bin and binary_key[2:4] == g_bin and binary_key[4:6] == b_bin

def make_text_img(fnt : ImageFont.ImageFont, text: str, text_size: int) -> Image.Image:
    """
    Generates image of text with the exact dimensions required by given font.
    """

    text_length = int(fnt.getlength(text))

    text_img = Image.new("RGB", (text_length, text_size), color="white")
    draw = ImageDraw.Draw(text_img)
    draw.text((0, 0), text=text, fill=(0, 255, 0), font=fnt)

    return text_img

def generate_key() -> int:
    """
    Generates 4 digit key.
    """
    return random.randint(1000, 9999)

def str2bin(text: str) -> list:
    """
    Converts each letter in a string to binary using ASCII encoding.
    """

    res = []

    for c in list(text):
        res += list(format(ord(c), 'b').zfill(8))

    return list(map(lambda x: int(x), res))