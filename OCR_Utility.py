import pytesseract
from PIL import Image
import io 
import os
import pdfminer.high_level
import cv2
import docx
import logging
from logging import StreamHandler, FileHandler


logging.basicConfig(level=logging.INFO, filename='ocr_log.txt')  # Log to a file
console_handler = StreamHandler()  # Add console handler
console_handler.setLevel(logging.DEBUG)  # Set verbosity for console
logger = logging.getLogger(__name__)
logger.addHandler(console_handler)


def ocr_from_image(image_file):
    logger.info("Starting OCR process for image: %s", image_file)
    try:
        logger.debug("Opening image file: %s", image_file)
        img = cv2.imread(image_file)

        max_width = 1024  # Adjust as needed
        if img.shape[1] > max_width:
            width_percent = max_width / img.shape[1]  # Simplified calculation
            height_size = int(img.shape[0] * width_percent)
            img = cv2.resize(img, (max_width, height_size), interpolation=cv2.INTER_AREA)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        img = cv2.bilateralFilter(img, 5, 9, 9)  # Uncomment for bilateral filtering
        
        # Convert to Pillow image for Tesseract
        img = Image.fromarray(img)

        # Change page segmentation mode if needed
        text_content = pytesseract.image_to_string(img, config='--psm 3',lang='eng')  
        logger.info("OCR extraction successful.")
        return text_content
    
    except FileNotFoundError as e:
        logger.error("Image file not found: %s", image_file)
        return ""  # Return an empty string on error
    
    except Exception as e:  # Catch other potential errors
        logger.error("An unexpected error occurred: %s", e)
        raise  # Re-raise for further handling

def ocr_from_pdf(pdf_file):
    logger.info("Starting OCR process for pdf: %s", pdf_file)
    try:
        logger.info("Opening PDF file: %s", pdf_file)
        with open(pdf_file, 'rb') as pdf_file_object:
            text = pdfminer.high_level.extract_text(pdf_file_object)
        logger.info("OCR Extraction Complete")    
        return text
    
    except(FileNotFoundError) as e:
        logger.error("Error Opening PDF file: %s",e) 
        return ""
    
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        raise 

def ocr_from_word(word_file): 
     logger.info("Starting OCR process for word: %s", word_file)
     try:
        logger.info("Opening Word file: %s", word_file)
        document = docx.Document(word_file)
        text = '\n'.join([paragraph.text for paragraph in document.paragraphs])
        logger.info("OCR extraction successful.")
        return text
    
     except (FileNotFoundError, ValueError) as e:
        logger.error("Error opening or processing Word file: %s", e)
        return ""  # Or return a default value or raise a custom exception
    
     except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        raise  # Re-raise the exception to allow further handling


"""
this method checks the type the type of 
document and calls the appropriate method for processing
"""
    
def perform_ocr(file_path):
    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() in ['.jpg', '.jpeg', '.png']:
        result = ocr_from_image(file_path)
        
    elif file_extension.lower() in ['.pdf']:
        result = ocr_from_pdf(file_path)

    elif file_extension.lower() in ['.doc','.docx']:
        result = ocr_from_word(file_path)

    else:
        print("File format not supported")

    return result

def write_to_txt_file(extracted_text_data, output_file_name):
    logger.info("Writing data to file {}".format(output_file_name))
    with open(output_file_name,'w') as f:
        f.write(extracted_text_data)
    logger.info("File Writing Completed")    


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