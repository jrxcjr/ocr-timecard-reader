import os
from dotenv import load_dotenv
from pdf2image import convert_from_path

import cv2
import numpy as np
import pytesseract

#Converts PDF to images
def convert_pdf_to_image(path):
    pdf_file = path

    pages = convert_from_path(pdf_file)
    
    return pages

#Deskew images in the Pdf that might be rotated or inverted.
def deskew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    coords = np.column_stack(np.where(gray > 0))
    angle = cv2.minAreaRect(coords)[-1]
    
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated

# Extract text from images in pdf
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

# Processes file conversion to text
def process_pdf_file(path):
    
    pages = convert_pdf_to_image(path)

    for page in pages:

        #deskew image from text
        preprocessed_page = deskew(np.array(page))

        #extract text using ocr
        text = extract_text_from_image(page)
        extracted_text.append(text)
    
    return print(extracted_text)


#Loaded path to file to be converted from env
load_dotenv()

#Save file to property
path = os.getenv('FILE_READ_PATH')

extracted_text = []

result = process_pdf_file(path)