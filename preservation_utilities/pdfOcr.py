import sys, os
import ocrmypdf
import shutil
import pytesseract
import io
from PyPDF2 import PdfFileMerger
import pdf2image
import PIL
import time

source = input("folder structure to process: ")
for dirpath, dirnames, filenames in os.walk(source):
    for filename in filenames:
        if filename.endswith(".pdf") and dirpath.endswith("preservation1"):
            target = dirpath.replace(dirpath.split("/")[-1],"presentation2")
            target = os.path.join(target,filename).replace("/./","/")
            filename1 = filename
            filename = os.path.join(dirpath, filename)
            if not os.path.exists(os.path.dirname(target)):
                os.makedirs(os.path.dirname(target), exist_ok=True)
            try:
                result = ocrmypdf.ocr(filename,target)
                if result == ocrmypdf.ExitCode.ok:
                    print(filename,"ocr'd and copy completed")
            except ocrmypdf.exceptions.PriorOcrFoundError:
                shutil.copy2(filename,target)
                shutil.copystat(filename,target)
                print(filename,"previously ocr'd, copied instead")
                continue
            except:
                '''print("error in ocr, copying to a neutral space to be fixed with acrobat")
                target = "./presentation2/" + filename1
                shutil.copy2(filename,target)
                shutil.copystat(filename,target)'''
                print(f"other methods failed for {filename}, trying tesseract")
                staging = "./staging/"
                images = pdf2image.convert_from_path(filename)
                counter = 0
                image_list = []
                for item in images:
                    image_to_save = staging + str(counter) + ".jpg"
                    im = item.save(image_to_save)
                    image_list.append(image_to_save)
                    counter += 1
                merger = PdfFileMerger()
                image_list.sort()
                for item in image_list:
                    pdf = pytesseract.image_to_pdf_or_hocr(item, extension="pdf")
                    pdf_file_in_memory = io.BytesIO(pdf)
                    merger.append(pdf_file_in_memory)
                for item in image_list:
                    os.remove(item)
                merger.write(target)
                merger.close()