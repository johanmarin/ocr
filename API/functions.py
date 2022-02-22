import os
import pytesseract
from PIL import Image
import fastapi 

def save_file(filepath, data):
  with open(filepath, 'wb') as f:
      f.write(data)

def text_from_image(filepath: str):   
    # perform OCR on the processed image
    text = pytesseract.image_to_string(Image.open(filepath))
    print('se obtiene el contenido del archivo como texto')
    # remove the processed image
    os.remove(filepath)
    return text
    