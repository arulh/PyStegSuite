from PIL import Image, ImageDraw, ImageFont 

def encode_stencil(img_path: str, text: str, text_size=75, text_coords=(50, 50)) -> None:
    """
    Encodes the text into the image using a stencil approach.
    """
    