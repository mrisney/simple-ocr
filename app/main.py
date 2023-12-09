from typing import Union
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import io
import cv2
import pytesseract

#https://medium.aiplanet.com/talk-to-websites-using-openai-langchain-and-chromadb-f7a8942b1261

from api import ocrapi, openaiapi



description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="Simple OCR API",
    description=description,
    summary="image  to text, summarization, question answering, and more",
    version="0.9.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "identifier": "MIT",
    },
)



origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/user")
def read_user():
    return api.read_user()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()

    # Convert the contents to a format suitable for OCR
    image_stream = io.BytesIO(contents)
    file_bytes = np.frombuffer(image_stream.read(), dtype=np.uint8)

    # Perform OCR on the image
    extracted_text = ocrapi.extract_text(file_bytes)
    answer = await openaiapi.query_gpt3(extracted_text)
   
    # Close the file
    await file.close()

    return {
        "filename": file.filename, 
        "message": f"File processed successfully {file.filename}",
        "extracted_text": extracted_text,
        "answer"    : answer
    }


