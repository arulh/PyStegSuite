from PIL import Image, ImageFont

from helper import encode_pixel, generate_key, make_text_img, str2bin, encode_lsb

def encode_text(encoded_text: str, img_path: str=None, img: Image.Image=None) -> tuple | ValueError:
    """
    Encodes the text into the image.

    Args:
        encoded_text (str): The text to be encoded into the image.
        img_path (str, optional): The path to the image file. Defaults to None.
        img (Image.Image, optional): The image object. Defaults to None.

    Returns:
        tuple | ValueError: A tuple containing the encoded image (Image.Image) and the length of the encoded text (int).

    Raises:
        ValueError: If neither img_path nor img is provided.
        ValueError: If the text does not fit in the image.

    Note:
        - At least one image argument (img_path or img) must be provided.
        - The image should be in RGB format.
        - The encoded text should fit within the image. If the length of the encoded text multiplied by 8 is greater than the number of pixels in the image, a ValueError is raised.
        - The function uses the least significant bit (LSB) technique to encode the text into the image pixels.

    Example:
        encoded_image, text_length = encode_text("Hello, world!", img_path="image.png")
    """
    
    # checks if at least one image argument is provided
    if (img_path == None and img == None):
        raise ValueError("MUST PROVIDE IMAGE ARGUMENT")
    
    if (img_path != None and img == None):
        img = Image.open(img_path).convert("RGB")
    else:
        # default to using img argument
        img = img.convert("RGB")

    length, height = img.getbbox()[2]-img.getbbox()[0], img.getbbox()[3]-img.getbbox()[1]
    num_pixels = length * height

    # checks if encoded_text can fit in the provided image
    if (len(encoded_text)*8 > num_pixels):
        raise ValueError("TEXT DOES NOT FIT IN IMAGE")
    
    # generate binary version of encoded_text
    bin_encodings = str2bin(encoded_text)

    curr = (0, 0)
    for b in bin_encodings:
        if (curr[0] == length):
            curr = (0, curr[1]+1)

        p = img.getpixel(curr)
        img.putpixel(curr, encode_lsb(p, b))

        curr = (curr[0]+1, curr[1])

    return img, len(encoded_text)

def encode_stencil(encoded_text: str,img_path: str=None, img: Image.Image=None, text_size=50, text_coords=(0, 0)) -> tuple | ValueError:
    """
    Encodes the text into the image as a stencil (symmetric cipher).

    Args:
        encoded_text (str): The text to be encoded into the image.
        img_path (str, optional): The path to the image file. Defaults to None.
        img (Image.Image, optional): The image object. Defaults to None.
        text_size (int, optional): The size of the text in pixels. Defaults to 50.
        text_coords (tuple, optional): The coordinates (x, y) where the top-left corner of the text will be placed on the image. Defaults to (0, 0).

    Returns:
        tuple | ValueError: A tuple containing the encoded image (Image.Image) and the key (int) used for encoding.

    Raises:
        ValueError: If neither img_path nor img argument is provided.
        ValueError: If the text does not fit on the image.
        ValueError: If the encoded text does not contain at least one character.
    """

    # checks if at least one image argument is provided
    if (img_path == None and img == None):
        raise ValueError("MUST PROVIDE IMAGE ARGUMENT")
    
    if (img_path != None and img == None):
        img = Image.open(img_path).convert("RGB")
    else:
        # default to using img argument
        img = img.convert("RGB")
    
    length, height = img.getbbox()[2]-img.getbbox()[0], img.getbbox()[3]-img.getbbox()[1]
    fnt = ImageFont.load_default(text_size)
    text_length = int(fnt.getlength(encoded_text))

    # check valid arguments
    if (text_length+text_coords[0] > length or text_size+text_coords[1] > height):
        raise ValueError("TEXT DOES NOT FIT ON IMAGE")
    elif (encoded_text.isspace()):
        raise ValueError("ENCODED TEXT MUST CONTAIN AT LEAST ONE CHARACTER")
    
    # generate stencil
    text_img = make_text_img(fnt, encoded_text, text_size)

    key = generate_key()

    for y in range(text_size):
        for x in range(text_length):
            if (text_img.getpixel((x, y)) == (0, 255, 0)):
                adjusted_coords = (x+text_coords[0], y+text_coords[1])
                img.putpixel(adjusted_coords, encode_pixel(img.getpixel(adjusted_coords), key))

    return img, key