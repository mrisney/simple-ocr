from typing import Union
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import io

from api import tesseractAPI, insuranceCardExtractAPI, registrationCardExtractAPI

description = """
Tesseract OCR, ChatGPT helps you do awesome stuff. 🚀

### ChatGPT Model 

Current Model **text-davinci-003**.

### Tesseract OCR version

You will be able to:

* **Persist data to Oracle Database ** (_not implemented_).
* **Analyze Voice Narrative ** (_not implemented_).
"""

app = FastAPI(
    title="MOANA Document Analysis API",
    description=description,
    summary="Image to Text, Text Extraction, Question Answering, and more",
    version="0.8.1 alpha",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Marc Risney",
        "url": "http://x-force.example.com/contact/",
        "email": "mrisney@itis-corp.com",
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

@app.post("/basic-ocr")
async def basic_ocr(file: UploadFile = File(...)):
    contents = await file.read()

    # Convert the contents to a format suitable for OCR
    image_stream = io.BytesIO(contents)
    file_bytes = np.frombuffer(image_stream.read(), dtype=np.uint8)

    # Perform OCR on the image
    extracted_text = tesseractAPI.extract_text(file_bytes)

    # Close the file
    await file.close()

    return {
        "filename": file.filename, 
        "message": f"OCR processed successfully {file.filename}",
        "extracted_text": extracted_text
    }

@app.post("/insurance-card-extract")
async def insurance_card_extract(file: UploadFile = File(...)):
    contents = await file.read()

    # Convert the contents to a format suitable for OCR
    image_stream = io.BytesIO(contents)
    file_bytes = np.frombuffer(image_stream.read(), dtype=np.uint8)

    # Perform OCR on the image
    extracted_text = tesseractAPI.extract_text(file_bytes)
    answer = await insuranceCardExtractAPI.query_gpt3(extracted_text)
   
    # Close the file
    await file.close()

    return {
        "filename": file.filename, 
        "message": f"File processed successfully {file.filename}",
        "extracted_text": extracted_text,
        "answer"    : answer
    }


@app.post("/registration_card_extract")
async def registration_card_extract(file: UploadFile = File(...)):
    contents = await file.read()

    # Convert the contents to a format suitable for OCR
    image_stream = io.BytesIO(contents)
    file_bytes = np.frombuffer(image_stream.read(), dtype=np.uint8)

    # Perform OCR on the image
    extracted_text = tesseractAPI.extract_text(file_bytes)

    # analyze with ChatGPT
    answer = await registrationCardExtractAPI.query_gpt3(extracted_text)
   
    # Close the file
    await file.close()

    return {
        "filename": file.filename, 
        "message": f"File processed successfully {file.filename}",
        "extracted_text": extracted_text,
        "answer"    : answer
    }


