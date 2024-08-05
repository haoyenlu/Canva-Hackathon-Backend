from fastapi import FastAPI
from fastapi import File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated

import io
from PIL import Image
import time
import base64
import rembg
import json

from utils import  image_to_svg, transparent_to_white, image_to_b64

class DescriptionItem(BaseModel):
    description: str = None
    num_image: int = None

class ImageItem(BaseModel):
    image: str = None
    blacklevel: float = None



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/healthz')
def health():
    '''Check health'''
    return "Connect Successfully"


@app.get("/")
def root():
    return "Hello World"

@app.post("/upload_image")
def upload_image(item: ImageItem):
    base64Image = item.image
    image = Image.open(io.BytesIO(base64.b64decode(base64Image)))
    nobgImage = rembg.remove(image)
    whitebgImage = transparent_to_white(nobgImage)
    svgImage = image_to_svg(whitebgImage,item.blacklevel)

    base64svg = base64.b64encode(svgImage.encode('ascii'))
    return {"svg":base64svg}
    


@app.post("/get_image")
def get_image(item: DescriptionItem):
    # Test return images

    img_list = [Image.open("./images/cat.jpg"),Image.open("./images/dog.jpg")]

    image_b64 = [image_to_b64(image) for image in img_list]

    return json.dumps(image_b64)

