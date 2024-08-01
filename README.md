# PyStegSuite

## Demo



## Installation

`pip install git+https://github.com/arulh/PyStegSuite.git`

### Original image

![image](https://github.com/arulh/PyStegSuite/assets/104797653/116a6ed9-f97f-4771-acfa-1a12e6d980b5)

### Encode image

``` python
from PIL import Image
from stegimage import encode_stencil, decode_stencil

im = Image.open("./resources/image.png")
encoded_im, key = encode_stencil("hello world", img=im, text_size=50, text_coords=(50, 50))
```
![output](https://github.com/arulh/PyStegSuite/assets/104797653/96b052dc-1154-4393-8f7f-afbd7e8d180e)

### Decode image

```python
decoded_im = decode_stencil(key, img=encoded_im)
```

![dec_img](https://github.com/arulh/PyStegSuite/assets/104797653/8c51a67e-6810-469d-bb65-98dfbafa9cfe)
