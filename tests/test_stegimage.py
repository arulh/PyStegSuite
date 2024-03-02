import sys
sys.path.append('../src/stegimage')

from PIL import ImageFont
import pytest
import random
import encoder
# import stegimage.decoder
import helper as h

def test_encode_stencil_exceptions() -> None:
    """
    Tests the exceptions of encode_stencil.
    """

    text_size = 10
    fnt = ImageFont.load_default(text_size)
    text = "Hello"
    text_length = int(fnt.getlength(text))
    rel_path = "resources/beach.png" # beach.png is 1024x1024 pixels

    # testing text_size
    try:
        encoder.encode_stencil(rel_path, text, text_size=text_size, text_coords=(0, 1024-text_size))
    except:
        pytest.fail("UNEXPECTED ERROR")

    with pytest.raises(ValueError) as execinfo:
        encoder.encode_stencil(rel_path, text, text_size=1025-text_size)
    assert str(execinfo.value) == "TEXT DOES NOT FIT ON IMAGE"

    # testing text_length
    try:
        encoder.encode_stencil(rel_path, text, text_size=text_size, text_coords=(1024-text_length, 0))
    except:
        pytest.fail("UNEXPECTED ERROR")

    with pytest.raises(ValueError) as execinfo:
        encoder.encode_stencil(rel_path, text, text_size=text_size,  text_coords=(1025-text_length, 0))
    assert str(execinfo.value) == "TEXT DOES NOT FIT ON IMAGE"

    # test invalid string
    with pytest.raises(ValueError) as execinfo:
        encoder.encode_stencil(rel_path, "   ")
    assert str(execinfo.value) == "ENCODED TEXT MUST CONTAIN AT LEAST ONE CHARACTER"

    with pytest.raises(ValueError) as execinfo:
        encoder.encode_stencil(rel_path, "\t\n")
    assert str(execinfo.value) == "ENCODED TEXT MUST CONTAIN AT LEAST ONE CHARACTER"

def test_helper_make_text_img() -> None:
    """
    Tests the proper dimensions of text image.
    """
    text_size = 50
    fnt = ImageFont.load_default(text_size)

    text_im1 = h.make_text_img(fnt, "Hello World", text_size)

    length, height = text_im1.getbbox()[2]-text_im1.getbbox()[0], text_im1.getbbox()[3]-text_im1.getbbox()[1]

    assert height == text_size
    assert length == 268 # specific to font

def test_helper_encode_pixel() -> None:
    """
    Testing encryption and decryption functions.
    """

    test_count = 5000

    for x in range(test_count):
        test_key = h.generate_key()
        pixel = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
        new_pixel = h.encode_pixel(pixel, test_key)

        assert h.is_encoded_pixel(new_pixel, test_key)

def test_helper_str2bin() -> None:
    """
    Testing string to binary conversion.
    """

    assert h.str2bin("h") == [0, 1, 1, 0, 1, 0, 0, 0]
    assert h.str2bin("x") == [0, 1, 1, 1, 1, 0, 0, 0]
    assert h.str2bin("V") == [0, 1, 0, 1, 0, 1, 1, 0]
    assert h.str2bin("hxV") == [0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0]
    assert h.str2bin(" ") == [0, 0, 1, 0, 0, 0, 0, 0]