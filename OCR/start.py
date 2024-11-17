from paddleocr import PaddleOCR
from PIL import Image
import numpy as np
from OCR.processor import getTotal

# Load the image directly from a file-like object
def process_image(file):
    
    # Initialize the PaddleOCR instance
    ocr = PaddleOCR(use_angle_cls=True, lang='en')  # 'en' for English, 'ch' for Chinese, etc.
    
    # Open the image using PIL
    image = Image.open(file.stream)
    print("dfhiu3hafhahd:",type(file))

    # Convert the image to a numpy array
    image_np = np.array(image)

    # Perform OCR on the image data
    result = ocr.ocr(image_np, cls=True)

    final = ""
    lines = []
    # Output the results
    for line in result[0]:
        final += line[1][0] + "\n"
        lines.append(line[1][0])
    
    return final, getTotal(lines)
