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

def text_to_coordinates(text: str) -> list:
    """
    Returns: list of coordinates to be encrypted.
    """

    res = []

    letter_coordinates = {
        'A': [(1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)],
        'B': [(1, 1), (2, 1), (1, 2), (2, 2), (1, 3), (2, 3), (1, 4), (2, 4)],
        'C': [(1, 1), (2, 1), (3, 1), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4)],
        'D': [(1, 1), (2, 1), (1, 2), (2, 2), (1, 3), (2, 3), (1, 4), (2, 4)],
        'E': [(1, 1), (2, 1), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4)],
        'F': [(1, 1), (2, 1), (1, 2), (1, 3), (1, 4), (2, 4)],
        'G': [(1, 1), (2, 1), (3, 1), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (3, 3)],
        'H': [(1, 1), (1, 2), (1, 3), (1, 4), (2, 2), (3, 1), (3, 2), (3, 3), (3, 4)],
        'I': [(1, 1), (2, 1), (3, 1), (2, 2), (2, 3), (1, 4), (2, 4), (3, 4)],
        'J': [(1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (2, 4)],
        'K': [(1, 1), (1, 2), (1, 3), (1, 4), (2, 3), (3, 2), (3, 4)],
        'L': [(1, 1), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4)],
        'M': [(1, 1), (1, 2), (1, 3), (1, 4), (2, 2), (3, 3), (4, 2), (5, 1), (5, 2), (5, 3), (5, 4)],
        'N': [(1, 1), (1, 2), (1, 3), (1, 4), (2, 2), (3, 3), (4, 4)],
        'O': [(1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)],
        'P': [(1, 1), (2, 1), (1, 2), (2, 2), (1, 3), (2, 3)],
        'Q': [(1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3), (3, 4)],
        'R': [(1, 1), (2, 1), (1, 2), (2, 2), (1, 3), (2, 3), (1, 4), (2, 4), (3, 3)],
        'S': [(1, 1), (2, 1), (1, 2), (1, 3), (2, 4), (3, 4)],
        'T': [(1, 1), (2, 1), (3, 1), (2, 2), (2, 3), (2, 4)],
        'U': [(1, 1), (1, 2), (1, 3), (1, 4), (2, 4), (3, 1), (3, 2), (3, 3), (3, 4)],
        'V': [(1, 1), (1, 2), (2, 3), (2, 4), (3, 1), (3, 2)],
        'W': [(1, 1), (1, 2), (1, 3), (1, 4), (2, 3), (3, 2), (4, 3), (5, 2), (6, 1), (6, 2), (6, 3), (6, 4)],
        'X': [(1, 1), (1, 4), (2, 2), (2, 3), (3, 1), (3, 4)],
        'Y': [(1, 1), (1, 2), (2, 3), (3, 1), (3, 2)],
        'Z': [(1, 1), (2, 1), (3, 1), (3, 2), (2, 3), (1, 4), (2, 4), (3, 4)],
    }

    for count, char in enumerate(text):
        temp = list(map(lambda x: (x[0]+count*10, x[1]), letter_coordinates[char.upper()]))

        for coord in temp:
            res.append((coord[0], coord[1]))

    return res