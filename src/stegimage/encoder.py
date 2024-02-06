from PIL import Image, ImageDraw, ImageFont

from helper import encode_pixel, generate_key

def encode_stencil(img_path: str, encoded_text: str, text_size=75, text_coords=(50, 50)) -> tuple | ValueError:
    """
    Encodes the text into the image using a stencil approach.

    Returns:
        Image object, key
    """
    
    img = Image.open(img_path).convert("RGBA")
    length, height = img.getbbox()[2]-img.getbbox()[0], img.getbbox()[3]-img.getbbox()[1]
    fnt = ImageFont.load_default(text_size)
    text_length = int(fnt.getlength(encoded_text))

    # check valid arguments
    if (text_size > height):
        raise ValueError("TEXT SIZE MUST FIT ON IMAGE")
    elif (text_coords[0] > length or text_coords[1] > height or text_coords[0] < 0 or text_coords[1] < 0):
        raise ValueError("TEXT COORDINATES NEED TO BE IN IMAGE")
    elif (encoded_text.isspace()):
        raise ValueError("ENCODED TEXT MUST CONTAIN AT LEAST ONE CHARACTER")
    
    text_img = Image.new("RGB", (text_length, text_size), color="white")
    
    draw = ImageDraw.Draw(text_img)
    
    draw.text((0, 0), text=encoded_text, fill=(0, 255, 0), font=fnt)

    key = generate_key()

    for y in range(text_size):
        for x in range(min(text_length, length)):
            if (text_img.getpixel((x, y)) == (0, 255, 0)):
                adjusted_coords = (x+text_coords[0], y+text_coords[1])
                img.putpixel(adjusted_coords, encode_pixel(img.getpixel(adjusted_coords), key))

    return img, key