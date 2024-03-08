from PIL import Image, ImageFont

from helper import encode_pixel, generate_key, make_text_img, str2bin, encode_lsb

def encode_text(img_path: str, encoded_text: str) -> tuple | ValueError:
    """
    Encodes the text into the image.

    Returns:
        encoded image (Image.Image), key (int)
    """

    img = Image.open(img_path).convert("RGB")
    length, height = img.getbbox()[2]-img.getbbox()[0], img.getbbox()[3]-img.getbbox()[1]
    num_pixels = length * height

    if (len(encoded_text)*8 > num_pixels):
        raise ValueError("TEXT DOES NOT FIT IN IMAGE")
    
    bin_encodings = str2bin(encoded_text)

    curr = (0, 0)
    for b in bin_encodings:
        if (curr[0] == length):
            curr = (0, curr[1]+1)

        p = img.getpixel(curr)
        img.putpixel(curr, encode_lsb(p, b))

        curr = (curr[0]+1, curr[1])

    return img, len(encoded_text)

def encode_stencil(img_path: str, encoded_text: str, text_size=50, text_coords=(0, 0)) -> tuple | ValueError:
    """
    Encodes the text into the image as a stencil.

    Returns:
        encoded image (Image.Image), key (int)
    """
    
    img = Image.open(img_path).convert("RGB")
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