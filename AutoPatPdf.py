from PIL import Image
import pytesseract
import argparse
import os
from pdf2image import convert_from_path
import sys

import urllib.request
import random
from urllib import request
from bs4 import BeautifulSoup as bs
import re
import json
import retrying
from user_agents import users


def FetchUrlPdf(patent_id=patent_id, headers, proxy_port=1081):
    url="http://patents.google.com/patent/{}".format(patent_id)
    request_ = request.Request(url, headers=headers)
    proxies = {'http': 'http://127.0.0.1:{}'.format(proxy_port),'https':'http://127.0.0.1:{}'.format(proxy_port)}
    proxy_hander = request.ProxyHandler(proxies)
    opener = request.build_opener(proxy_hander)
    response = opener.open(request_, timeout = 60)
    soup = bs(response, "html.parser")
    link = soup.find("a", text = "Download PDF").get("href")
    response.close()
    return link

def save_pdf(link, patent_id):
    pdf_file = urllib.request.urlopen(link, timeout = 60)
    with open("{}.pdf".format(patent_id), "wb") as f:
        f.write(pdf_file.read())

def PdfTotxt(patent_id,outfile=''):
    PDF_file = patent_id+'.pdf'
    pages = convert_from_path(PDF_file, 500)   # tranform PDF to JPG
    image_counter = 1
    for page in pages:
        filename = "page_"+str(image_counter)+".jpg"
        page.save(filename, 'JPEG')
        image_counter = image_counter + 1
    
    filelimit = image_counter
    outfile = patent_id+'_total.txt'
    with open(outfile, "w") as f:
        for i in range(1, filelimit):
            filename = "page_"+str(i)+".jpg"
            text = str(((pytesseract.image_to_string(Image.open(filename)))))
            text = text.replace('-\n', '')
            f.write(text)

def ExtractIupac(patent_id,outfile='outfile.csv'):
     txtname=patent_id+'_total.txt'
     rc=re.compile(r'^[aA-Z"0\>\-\\\)/\'’”]')
     rb=re.compile(r'^[0-9][0-9%]')
     ra=re.compile(r'^\w$')
     outfile=patent_id+'.csv'
     f2 = open(outfile, 'w', encoding='utf-8')   
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
        
def AutoPatPdf(patent_id,outfile_txt='Example.txt',outfile_csv='Example.csv'):  
    headers = {"User-Agent":random.choice(users),}
    link=FetchUrlPdf(patent_id=patent_id, headers, proxy_port=1081)
    save_pdf(link, patent_id)
    PdfTotxt(patent_id,outfile=outfile_txt)
    ExtractIupac(patent_id,outfile=outfile_csv)

if __name__ == "__main__":
    patent_id = "US20200048241A1"
    AutoPatPdf(patent_id,outfile_txt='Example.txt',outfile_csv='Example.csv')
