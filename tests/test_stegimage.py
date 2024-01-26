import sys
sys.path.append('../src/')

import random
import timeit
from stegimage.helper import encode_pixel, is_encoded_pixel, generate_key

def test_helper() -> None:
    """
    Tests all functions contained in helper.py
    """

    test_count = 5000

    for x in range(test_count):
        test_key = generate_key()
        pixel = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
        new_pixel = encode_pixel(pixel, test_key)
        try:
            assert is_encoded_pixel(new_pixel, test_key)
        except AssertionError:
            print("\x1b[5;30;41m" + "TEST CASE FAILED" + "\x1b[0m")
            sys.exit()


if __name__ == "__main__":
    start = timeit.default_timer()


    test_helper()


    stop = timeit.default_timer()
    print("\x1b[6;30;42m" + "ALL TESTS PASSED" + "\x1b[0m")
    print(f"Execution time: {(stop - start):.3f} seconds")