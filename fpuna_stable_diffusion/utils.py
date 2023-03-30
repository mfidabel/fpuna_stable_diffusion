from PIL import Image
import requests
from io import BytesIO
from IPython.display import HTML
from base64 import b64encode

def visualize_video_colab(video_path):
    mp4 = open(video_path,'rb').read()
    data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
    return HTML("""
    <video width=400 controls>
        <source src="%s" type="video/mp4">
    </video>
    """ % data_url)

# https://huggingface.co/blog/stable_diffusion
def image_grid(imgs, rows, cols):
    assert len(imgs) == rows*cols

    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols*w, rows*h))
    grid_w, grid_h = grid.size
    
    for i, img in enumerate(imgs):
        grid.paste(img, box=(i%cols*w, i//cols*h))
    return grid


def download_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content)).convert("RGB")

def agregar_margen(img, margen = (128, 128, 128, 128), color = 0):
    izq, der, arriba, abajo = margen
    width, height = img.size
    new_width = width + izq + der
    new_height = height + arriba + abajo
    resultado = Image.new(img.mode, (new_width, new_height), color)
    resultado.paste(img, (izq, arriba))
    mascara = Image.new(img.mode, (new_width, new_height), (255, 255, 255))
    mascara.paste(Image.new(img.mode, (width, height), (0, 0, 0)), (izq, arriba))
    
    return resultado, mascara