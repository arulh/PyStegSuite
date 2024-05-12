# from example_package.src.stegimage import encoder as enc
# from stegimage.encoder import encode_stencil
import stegimage.encoder as encoder
from PIL import Image

im = Image.open("./examples/image.png")

eim, k = encoder.encode_stencil("hello", img=im)

print(k)
