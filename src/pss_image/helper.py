import random

def encode_pixel(pixel: tuple, key: int) -> tuple:
    """
    Encodes the key into the lower order bits of the pixel (r, g, b, a).

    Returns:
        Encoded pixel as tuple.
    """

    key = key%64

    # extract RGB values from pixel
    r, g, b = pixel[0], pixel[1], pixel[2]

    # convert key to a binary string
    binary_key = bin(key)[2:].zfill(6)

    # encode the lower order bits of the RGB values with the key
    r = (r & 0b1111111100) | int(binary_key[0:2], 2)
    g = (g & 0b1111111100) | int(binary_key[2:4], 2)
    b = (b & 0b1111111100) | int(binary_key[4:6], 2)

    return (r, g, b, 255)

def generate_key() -> int:
    """
    Returns:
        Generated 4 digit key.
    """
    return random.randint(1000, 9999)