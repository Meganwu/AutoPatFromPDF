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
     rc=re.compile(r'^[aA-Z"0\>\-\\\)/\'’”]')
     rb=re.compile(r'^[0-9][0-9%]')
     ra=re.compile(r'^\w$')
     f2 = open(ourfile, 'w', encoding='utf-8')   
     with open(txtname,encoding='utf-8') as f_origin:
       for line in f_origin.readlines():
          if re.findall(pattern_exampl, line):
            line = re.sub('^','\n',line)
            line = re.sub('$\n','  ',line)
            f2.write(line)
          else:
            if rc.findall(line) or rb.findall(line) or ra.findall(line):
                line = line
                print(line)
            else:   
               line = line.strip()
               line = re.sub('[\n]+','\n',line)
               line = re.sub('—','-',line)
#              line = re.sub('s+','',line)
               line = re.sub(' ','',line)
               line = re.sub('I(?<=[\'\-])','1',line)
               line = re.sub('(?<=-)l','1',line)
               line = line.split('and')[0]
               line = re.sub('(?<=[a-zA-Z])1(?<=[a-zA-Z])','l',line)
               line = re.sub('[Il]RS','1RS',line)
#               line = re.sub('and(?<=[\(\w+])','',line)
#             line = ''.join(line.split())
#              print(line)
               f2.write(line)    
      f2.close()           

if __name__ == "__main__":
    patent_id = "US20200048241A1"
    Main(patent_id, get_smiles=True, saved_dir='./test/temp', notes="")
