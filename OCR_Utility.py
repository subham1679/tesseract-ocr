import pytesseract
from PIL import Image
import io 
import os
import pdfminer.high_level
import cv2


# def ocr_from_image(image_file):
#     img = Image.open(image_file)
#     text_content = pytesseract.image_to_string(img)
#     return text_content



# def ocr_from_image(image_file):
#     img = cv2.imread(image_file)

#     max_width = 1024  # Adjust as needed
#     if img.shape[1] > max_width:
#         width_percent = (max_width / float(img.shape[1]))
#         height_size = int((float(img.shape[0]) * float(width_percent)))
#         img = cv2.resize(img, (max_width, height_size), interpolation=cv2.INTER_AREA)

#     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
#     img = cv2.medianBlur(img, 5)  # Apply median filtering
#     img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  # Otsu's thresholding

#     # Convert to Pillow image for Tesseract
#     img = Image.fromarray(img)

#     text_content = pytesseract.image_to_string(img)
#     return text_content

def ocr_from_image(image_file):
    img = cv2.imread(image_file)

    max_width = 1024  # Adjust as needed
    if img.shape[1] > max_width:
        width_percent = (max_width / float(img.shape[1]))
        height_size = int((float(img.shape[0]) * float(width_percent)))
        img = cv2.resize(img, (max_width, height_size), interpolation=cv2.INTER_AREA)

    # Potential adjustments:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    img = cv2.bilateralFilter(img, 5, 9, 9)  # Uncomment for bilateral filtering
    

    # Convert to Pillow image for Tesseract
    img = Image.fromarray(img)

    text_content = pytesseract.image_to_string(img, config='--psm 3',lang='eng')  # Change page segmentation mode if needed

    return text_content

def ocr_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as pdf_file_object:
        text = pdfminer.high_level.extract_text(pdf_file_object)
    return text

def perform_ocr(file_path):
    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() in ['.jpg', '.jpeg', '.png']:
        result = ocr_from_image(file_path)
    elif file_extension.lower() in ['.pdf']:
        result = ocr_from_pdf(file_path)
    else:
        print("File format not supported")

    return result

def write_to_txt_file(extracted_text_data, output_file_name):
    with open(output_file_name,'w') as f:
        f.write(extracted_text_data)
