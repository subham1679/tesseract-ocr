import OCR_Utility as ocu
import time


file_path = 'your file path'
start_time = time.time()
result_text = ocu.perform_ocr(file_path)
end_time = time.time()
# print(result_text)

ocu.write_to_txt_file(result_text,'destiantion file path')
print("time elapsed is --> {:.2f} seconds".format(end_time-start_time))