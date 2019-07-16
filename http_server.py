# Licensed under the MIT license
# Copyright (c) 2016 Yves Van Belle (yvanbelle@brother.be)

import os
import sys
import glob
import socket
import cherrypy
from xml.dom.minidom import parseString
from mail_pdf_att import mail_with_pdf
import tesseract_ocr
import barcode2pdfs
import move_files


HTTP_PORT = 9999
IP_ADDRESS = socket.gethostbyname(socket.gethostname())


class Bsi(object):
    @staticmethod
    def get_xml_file(filename):
        with open('xml/' + filename) as f:
            xml_data = f.read()
        f.close()
        return xml_data

    # Main BSI screen
    @cherrypy.expose
    def index(self, **kwargs):
        main_menu = self.get_xml_file('linkscreen_img.xml')
        return main_menu

    # Scan to CIFS interface
    @cherrypy.expose
    def orderscan(self, **kwargs):
        return self.get_xml_file('orderscan.xml')

    # Scan to CIFS actual scan
    @cherrypy.expose
    def scan2cifs(self, **kwargs):
        scan2cifs = self.get_xml_file('scan2cifs.xml')
        scan2cifs = scan2cifs.replace('cifsserver_ip', cifsserver_ip)
        scan2cifs = scan2cifs.replace('cifsserver_share', cifsserver_share)
        scan2cifs = scan2cifs.replace('cifsuser_loging', cifsuser_loging)
        scan2cifs = scan2cifs.replace('cifsuser_passwd', cifsuser_passwd)
        return scan2cifs

    # Scan to email - email send by Brother device
    @cherrypy.expose
    def scan2mail(self, **kwargs):
        scan2mail = self.get_xml_file('scan2mail.xml')
        scan2mail = scan2mail.replace('email_address', email_address)
        return scan2mail

    # Scan to FTP server - Scan JPEG files to OCR later
    @cherrypy.expose
    def scan2ocr(self, **kwargs):
        scan2ocrftp = self.get_xml_file('scan2ocr.xml')
        scan2ocrftp = scan2ocrftp.replace('ftpipaddress', ftpserver_ip)
        return scan2ocrftp

    # OCR JPEG files and create 1 PDF
    @cherrypy.expose
    def ocr_and_pdf(self, **kwargs):
        working_dir = os.getcwd()
        os.chdir(ftpserver_dir)
        tesseract_ocr.ocr_pdf_merge()
        os.chdir(working_dir)
        return self.get_xml_file('end.xml')

    # Scan to FTP server
    @cherrypy.expose
    def scan2ftp(self, **kwargs):
        post_data = (kwargs['xml'])
        order_number = post_data[(post_data.find('<Value>') + len('<Value>')):post_data.find('</Value>')]
        scan2ftp = self.get_xml_file('scan2ftp.xml')
        scan2ftp = scan2ftp.replace('ordernr', order_number)
        scan2ftp = scan2ftp.replace('ftpipaddress', ftpserver_ip)
        return scan2ftp

    # Scan to multiple emails - interface
    @cherrypy.expose
    def selector(self, **kwargs):
        sel = self.get_xml_file('selector.xml')
        return sel

    # Scan to multiple emails - extraction of email addresses & scan attachment to FTP server
    emaillist = ''

    @cherrypy.expose
    def selectoraction(self, **kwargs):
        xmldata = parseString(kwargs['xml'])
        for selected in xmldata.getElementsByTagName('Value'):
            email = selected.toxml()
            email = email[(email.find('<Value>')+len('<Value>')):email.find('</Value>')]
            self.emaillist = self.emaillist + email + ';'
        scan_att = self.get_xml_file('scan_selector_att.xml')
        scan_att = scan_att.replace('ftpserver_ip', ftpserver_ip)
        return scan_att

    # Scan to multiple emails - sending email via SMTP server with the attachment
    @cherrypy.expose
    def selectoraction2(self, **kwargs):
        from_email_address = 'brother.bsi@brother.be'
        to_email_address = self.emaillist
        email_subject = 'BSI send email with attachment'

        # Get file to attach
        brother_bsi_files = ftpserver_dir + os.sep + 'BrotherBSI*.pdf'
        brother_bsi_files = glob.glob(brother_bsi_files)
        attachment = brother_bsi_files[0]

        email_body = '''BSI email with PDF attachment

        Scan with BSI to file, then send email(s) from server with PDF attachment.'''

        mail_with_pdf(smtpserver, from_email_address, to_email_address, email_subject, attachment, email_body)

        # Remove scanned file
        working_dir = os.getcwd()
        os.chdir(ftpserver_dir)
        for file in brother_bsi_files:
            os.remove(file)
        os.chdir(working_dir)

        # Create message with email addresses
        msg = self.get_xml_file('message_with_image.xml')
        email_addresses = self.emaillist.split(';')
        email_addresses = str.join(' ', email_addresses)
        msg = msg.replace('EMAILS', email_addresses)
        self.emaillist = ''
        return msg

    # Scan pages with QR codes - scan pages to FTP server
    @cherrypy.expose
    def scan_qrcodes(self, **kwargs):
        qr_code = self.get_xml_file('scan_qrcodes.xml')
        qr_code = qr_code.replace('ftpserver_ip', ftpserver_ip)
        return qr_code

    # Scan pages with QR codes - convert JPG images to PDF files - move to the PDF files correct directory
    @cherrypy.expose
    def qrimages2pdfs(self, **kwargs):
        barcode2pdfs.createpdfs(ftpserver_dir)  # convert JPG images to PDF files
        move_files.move_files(ftpserver_dir)  # move PDF files to the correct directory
        end = self.get_xml_file('end.xml')
        return end

    # Read RfID Card
    @cherrypy.expose
    def read_rfid(self, **kwargs):
        readrfid = self.get_xml_file('read_rfid.xml')
        return readrfid

    # Show message with RFID card number
    @cherrypy.expose
    def show_rfidnr(self, **kwargs):
        post_data = (kwargs['xml'])
        rfid_number = post_data[(post_data.find('<Value>') + len('<Value>')):post_data.find('</Value>')]
        showrfidnr = self.get_xml_file('show_rfidnr.xml')
        showrfidnr =  showrfidnr.replace('rfidnumber', rfid_number)
        return showrfidnr


def run():
    print(r'Starting HTTP server: http://' + IP_ADDRESS + ':' + str(HTTP_PORT) + r'/')
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.server.socket_port = HTTP_PORT
    conf = {
        '/img': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(os.path.dirname(__file__), 'img')
        }
    }
    cherrypy.quickstart(Bsi(), config=conf)

if __name__ == "__main__":
    ftpserver_ip = sys.argv[1]
    ftpserver_dir = sys.argv[2]
    cifsserver_ip = sys.argv[3]
    cifsserver_share = sys.argv[4]
    cifsuser_loging = sys.argv[5]
    cifsuser_passwd = sys.argv[6]
    smtpserver = sys.argv[7]
    email_address = sys.argv[8]

    run()
