import OCR_Utility as ocu
import time


# file_path = '/home/shubhambhardwaj/Downloads/4293197_22043_TEST.pdf'
file_path = '/home/shubhambhardwaj/Pictures/word-1024x547.png'
start_time = time.time()
result_text = ocu.perform_ocr(file_path)
end_time = time.time()
print(result_text)

ocu.write_to_txt_file(result_text,'/home/shubhambhardwaj/Downloads/Test_Image_2.txt')
print(f"time elapsed is --> {end_time-start_time} seconds")