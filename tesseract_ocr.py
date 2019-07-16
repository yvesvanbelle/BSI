# Licensed under the MIT license
# Copyright (c) 2016 Yves Van Belle (yvanbelle@brother.be)

import os
import platform
import subprocess
from pdftools import pdf_merge


def tesseract_ocr(jpgfile):
    try:
        if platform.system() == 'Darwin':
            subprocess.check_output([r'/usr/local/bin/tesseract', jpgfile,
                                     jpgfile, 'pdf'], stderr=subprocess.STDOUT)
        elif platform.system() == 'Windows':
            subprocess.check_output([r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe', jpgfile,
                                     jpgfile, 'pdf'], stderr=subprocess.STDOUT)
        elif platform.system() == 'Linux':
            subprocess.check_output([r'/usr/bin/tesseract', jpgfile,
                                     jpgfile, 'pdf'], stderr=subprocess.STDOUT)
    except Exception as e:
        print(e)


def ocr_pdf_merge():
    jpg_files = [f for f in os.listdir('.') if os.path.isfile(f) and f.startswith('page') and f.endswith('.jpg')]
    for jpg_file in jpg_files:
        tesseract_ocr(jpg_file)
        os.remove(jpg_file)

    pdf_files = [f for f in os.listdir('.') if os.path.isfile(f) and f.startswith('page') and f.endswith('.pdf')]
    pdf_merge(pdf_files, 'ocred_document.pdf', delete=True)


if __name__ == '__main__':
    workdir = '/Users/yvesvanbelle/Brother'
    os.chdir(workdir)
    ocr_pdf_merge()
