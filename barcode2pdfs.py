# Licensed under the MIT license
# Copyright (c) 2016 Yves Van Belle (yvanbelle@brother.be)

import os
import glob
import subprocess
import platform
from fpdf import FPDF


def zbarimg(file):
    try:
        if platform.system() == 'Darwin':
            barcode = subprocess.check_output(["/usr/local/bin/zbarimg", "-q", file],
                                              stderr=subprocess.STDOUT)
        elif platform.system() == 'Windows':
            barcode = subprocess.check_output([r"C:\Program Files (x86)\ZBar\bin\zbarimg.exe", "-q", file],
                                              stderr=subprocess.STDOUT)
        elif platform.system() == 'Linux':
            # zbarimg from deb package zbartools
            barcode = subprocess.check_output(["/usr/bin/zbarimg", "-q", file], stderr=subprocess.STDOUT)
        barcode = str(barcode)
        barcode = barcode.split(':')[1]
        barcode = barcode.split('\\')[0]
        return barcode
    except:
        return 'NoBarcode'


def get_scan_date_number(file):
    scan_date_number = file.split('.')[0]
    scan_date_number = scan_date_number.split('_')
    scan_date_number = scan_date_number[1] + '_' + scan_date_number[2]
    return scan_date_number


def createpdfs(directory):
    pwd = os.getcwd()
    os.chdir(directory)

    pdf = FPDF()
    pdfname = None

    for f in glob.glob("*.jpg"):
        barcode = zbarimg(f)
        if barcode != 'NoBarcode':
            if pdfname != None and pdfname != barcode:
                pdf.output(pdfname + '_' + get_scan_date_number(f) + '.pdf', 'F')
                pdf.close()
            pdfname = barcode
            pdf = FPDF()
            pdf.add_page('Portrait')
            pdf.image(f, 0, 0, 210, 297)
            os.remove(f)
        elif barcode == 'NoBarcode':
            pdf.add_page('Portrait')
            pdf.image(f, 0, 0, 210, 297)
            os.remove(f)
    pdf.output(pdfname + '_' + get_scan_date_number(f) + '.pdf', 'F')
    pdf.close()

    os.chdir(pwd)

if __name__ == "__main__":
    directory = r"/Users/yvesvanbelle/Desktop/"
    createpdfs(directory)
