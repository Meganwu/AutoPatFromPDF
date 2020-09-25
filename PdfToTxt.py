from PIL import Image
import pytesseract
import argparse
import os
from pdf2image import convert_from_path
import sys

def PdfTotxt(pdfname,outfile='outfile.txt'):
    PDF_file = pdfname
    pages = convert_from_path(PDF_file, 500)   # tranform PDF to JPG
    image_counter = 1
    for page in pages:
        filename = "page_"+str(image_counter)+".jpg"
        page.save(filename, 'JPEG')
        image_counter = image_counter + 1
    
    filelimit = image_counter
    outfile = outfile
    with open(outfile, "w") as f:
        for i in range(1, filelimit):
            filename = "page_"+str(i)+".jpg"
            text = str(((pytesseract.image_to_string(Image.open(filename)))))
            text = text.replace('-\n', '')
            f.write(text)

def ExtractIupac(txtname,outfile='outfile.csv'):
    with open(txtname,encoding='utf-8') as f_origin:
         for line in f_origin:

if __name__ == "__main__":
    patent_id = "US20200048241A1"
    Main(patent_id, get_smiles=True, saved_dir='./test/temp', notes="")
