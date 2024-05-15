import gradio as gr
from stegimage import encoder, decoder

def encode_interface(image, message):
    print("encoding image")
    eim, key = encoder.encode_stencil(message, img=image)

    return eim, key

def decode_interface(image, key):
    print("decoding image")
    dim = decoder.decode_stencil(key, img=image)

    return dim


with gr.Blocks() as demo:
    image = gr.Image(type='pil')
    message = gr.Textbox()
    encode_btn = gr.Button("Encode")
    encoded_img = gr.Image(format="png")
    key = gr.Number("key")

    encode_btn.click(encode_interface, inputs=[image, message], outputs=[encoded_img, key])

    eimg = gr.Image(type="pil")
    dkey = gr.Number("key")
    decode_btn = gr.Button("Decode")
    dimg = gr.Image(type='pil')

    decode_btn.click(decode_interface, inputs=[eimg, dkey], outputs=dimg)

demo.launch()