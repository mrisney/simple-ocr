import io
import logging
import numpy as np

from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from api import openaiAnalysisAPI, tesseractAPI

# Set up basic logging
logging.basicConfig(level=logging.INFO)


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

#app.mount("/api", app)
app.mount("/ui", StaticFiles(directory="ui", html=True), name="ui")

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

@app.post("/ocr_openai_analysis")
async def ocr_openai_analysis(file: UploadFile = File(...)):
    logging.info(f"document being uploaded: {file.filename}")
    contents = await file.read()

    # Convert the contents to a format suitable for OCR
    image_stream = io.BytesIO(contents)
    file_bytes = np.frombuffer(image_stream.read(), dtype=np.uint8)

    # Perform OCR on the image
    ocr_extracted_text = tesseractAPI.extract_text(file_bytes)
    logging.info(f"ocr text from document: {ocr_extracted_text}")

     # Analyze with OpenAI chatGPT
    response = await openaiAnalysisAPI.query_gpt3(ocr_extracted_text)
    logging.info(f"Openai Analysis response: {response}")
    
    # Close the file
    await file.close()

    return {
        "filename": file.filename, 
        "message": f"File processed successfully {file.filename}",
        "extracted_text": ocr_extracted_text,
        "answers": response.get('question_answer_pairs', [])
    }


