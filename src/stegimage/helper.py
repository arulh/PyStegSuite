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

    return (encoded_r, encoded_g, encoded_b, 255)

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

    r = str(bin((r & 0b1111111100) | int(binary_key[0:2], 2)))
    g = str((g & 0b1111111100) | int(binary_key[2:4], 2))
    b = str((b & 0b1111111100) | int(binary_key[4:6], 2))

    print(binary_key[0:2])
    print(r)

    return binary_key[0:2] == r and binary_key[2:4] == g and binary_key[4:6] == b

def generate_key() -> int:
    """
    Generates 4 digit key.
    """
    return random.randint(1000, 9999)


pixel = (234, 50, 168, 255)
new_pixel = encode_pixel(pixel, 8888)
is_encoded_pixel(new_pixel, 8888)