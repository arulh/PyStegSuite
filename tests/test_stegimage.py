import sys
sys.path.append('../src/stegimage')

import pytest
import random
import encoder
# import stegimage.decoder
from helper import generate_key, encode_pixel, is_encoded_pixel

def test_encode_stencil() -> None:
    """
    Tests the assertions of encode_stencil.
    """

    try:
        # beach.png is 1024x1024 pixels
        encoder.encode_stencil("resources/beach.png", "Hello World", text_size=1024)
    except:
        pytest.fail("UNEXPECTED ERROR")

    with pytest.raises(ValueError) as execinfo:
        encoder.encode_stencil("resources/beach.png", "Hello World", text_size=1025)
    assert str(execinfo.value) == "TEXT SIZE MUST FIT ON IMAGE"


def test_helper() -> None:
    """
    Tests all functions contained in helper.py
    """

    test_count = 5000

    for x in range(test_count):
        test_key = generate_key()
        pixel = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
        new_pixel = encode_pixel(pixel, test_key)

        assert is_encoded_pixel(new_pixel, test_key)