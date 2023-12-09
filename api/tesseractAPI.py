import pytesseract
import cv2
import numpy as np

def extract_text(image_bytes):
    # Convert bytes to an image
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use Tesseract to OCR the image
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text