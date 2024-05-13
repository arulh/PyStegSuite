from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
from stegimage import encoder, decoder
import io
import os

app = FastAPI()

dir = os.path.dirname(__file__)
app.mount("/static", StaticFiles(directory=dir), name="static")

@app.post("/encode/", response_class=HTMLResponse)
async def encode_image(string: str= Form(), image: UploadFile = File()):
    # Processing the image
    image = Image.open(io.BytesIO(await image.read()))
    # Your encoding logic here...
    eim, key = encoder.encode_stencil(string, img=image)
    
    eim.save(f"{dir}/encoded_img.png")
    content = f"<html><body><h1>{key}</h1><img src='/static/encoded_img.png'></body></html>"
    return HTMLResponse(content=content)

@app.post("/decode/", response_class=HTMLResponse)
async def decode_image(key: str = Form(), image: UploadFile = File()):
    # Processing the image
    image = Image.open(io.BytesIO(await image.read()))
    # Your decoding logic here...
    dim = decoder.decode_stencil(int(key), img=image)
    dim.save(f"{dir}/decoded_img.png")
    return f"<html><body><img src='/static/decoded_img.png'></body></html>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
