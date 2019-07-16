# Licensed under the MIT license
# Copyright (c) 2016 Yves Van Belle (yvanbelle@brother.be)

from tkinter import *
import os
import sys
import socket
import subprocess
import smtp


class Application(Frame):
    ftpid = None
    httpid = None

    def start_bsi(self):
        start_directory = os.path.dirname(os.path.abspath(__file__))

        ftpd = start_directory + os.sep + 'ftp_server.py'
        ftpdargs = [sys.executable, ftpd,
                    self.ftpsrvEntry.get(), self.ftpdirEntry.get()]
        Application.ftpid = subprocess.Popen(ftpdargs)

        httpd = start_directory + os.sep + 'http_server.py'
        httpdargs = [sys.executable, httpd,
                     self.ftpsrvEntry.get(), self.ftpdirEntry.get(),
                     self.cifssrvEntry.get(), self.cifsshareEntry.get(),
                     self.loginEntry.get(), self.passwdEntry.get(),
                     self.smtpsrvEntry.get(),
                     self.emailaddressEntry.get()]
        Application.httpid = subprocess.Popen(httpdargs)

        self.start['state'] = DISABLED
        self.stop['state'] = NORMAL

    def stop_bsi(self):
        Application.ftpid.kill()
        print('Stopping FTP server')

        Application.httpid.kill()
        print('Stopping HTTP server')

        self.start['state'] = NORMAL
        self.stop['state'] = DISABLED

    def quit_bsi(self):
        if self.start['state'] == DISABLED:
            self.stop_bsi()
        self.quit()


    def create_widgets(self):
        self.canvas_top = Canvas(root)

        self.ftpsrvLabel = Label(self.canvas_top, text='IP address HTTP/FTP server:')
        self.ftpsrvLabel.pack(padx=10, anchor="w")
        self.ftpsrvEntry = Entry(self.canvas_top, fg='blue')
        self.hostip = socket.gethostbyname(socket.gethostname())
        self.ftpsrvEntry.insert(0, self.hostip)
        self.ftpsrvEntry['state'] = DISABLED
        self.ftpsrvEntry.pack()

        self.ftpdirLabel = Label(self.canvas_top, text='Scan directory FTP server:')
        self.ftpdirLabel.pack(padx=10, anchor="w")
        self.scandir = os.path.expanduser("~") + os.sep + "Brother"
        self.ftpdirEntry = Entry(self.canvas_top, fg='blue')
        self.ftpdirEntry.insert(0, self.scandir)
        self.ftpdirEntry.pack()

        self.cifssrvLabel = Label(self.canvas_top, text='IP address CIFS/SMB server:')
        self.cifssrvLabel.pack(padx=10, anchor="w")
        self.cifssrvEntry = Entry(self.canvas_top, fg='blue')
        self.cifssrvEntry.insert(0, self.hostip)
        self.cifssrvEntry.pack()

        self.cifsshareLabel = Label(self.canvas_top, text='CIFS/SMB share name:')
        self.cifsshareLabel.pack(padx=10, anchor="w")
        self.cifsshareEntry = Entry(self.canvas_top, fg='blue')
        self.cifsshareEntry.insert(0, "brother")
        self.cifsshareEntry.pack()

        self.loginLabel = Label(self.canvas_top, text='Windows login:')
        self.loginLabel.pack(padx=10, anchor="w")
        userhome = os.path.expanduser('~')
        login = os.path.split(userhome)[-1]
        self.loginEntry = Entry(self.canvas_top, fg='blue')
        self.loginEntry.insert(0, login)
        self.loginEntry.pack()

        self.passwdLabel = Label(self.canvas_top, text='Windows password:')
        self.passwdLabel.pack(padx=10, anchor="w")
        self.passwdEntry = Entry(self.canvas_top, show='*', fg='blue')
        self.passwdEntry.insert(0, "password")
        self.passwdEntry.pack()

        self.smtpsrvLabel = Label(self.canvas_top, text='SMTP server:')
        self.smtpsrvLabel.pack(padx=10, anchor="w")
        #smtp.set_proxy('10.10.129.129','8080')
        self.smtpsrv = smtp.get_smtp()
        self.smtpsrvEntry = Entry(self.canvas_top, fg='blue')
        self.smtpsrvEntry.insert(0, self.smtpsrv)
        self.smtpsrvEntry.pack()
        self.canvas_top.pack()

        self.emailaddressLabel = Label(self.canvas_top, text='E-mail address:')
        self.emailaddressLabel.pack(padx=10, anchor="w")
        self.emailaddress = 'email.name@provider.eu'
        self.emailaddressEntry = Entry(self.canvas_top, fg='blue')
        self.emailaddressEntry.insert(0, self.emailaddress)
        self.emailaddressEntry.pack()

        self.canvas_bottom = Canvas(root)

        self.start = Button(self.canvas_bottom)
        self.start["text"] = "Start"
        self.start["padx"] = 10
        self.start["pady"] = 10
        self.start["fg"] = "darkgreen"
        self.start["command"] = self.start_bsi
        self.start.pack({"side": "left", "padx": 20, "pady": 10})

        self.stop = Button(self.canvas_bottom)
        self.stop["text"] = "Stop",
        self.stop["padx"] = 10
        self.stop["pady"] = 10
        self.stop["fg"] = "red"
        self.stop["state"] = DISABLED
        self.stop["command"] = self.stop_bsi
        self.stop.pack({"side": "left", "padx": 20, "pady": 10})

        self.quitbsi = Button(self.canvas_bottom)
        self.quitbsi["text"] = "Quit",
        self.quitbsi["padx"] = 10
        self.quitbsi["pady"] = 10
        self.quitbsi["fg"] = "red"
        self.quitbsi["state"] = NORMAL
        self.quitbsi["command"] = self.quit_bsi
        self.quitbsi.pack({"side": "left", "padx": 20, "pady": 10})

        self.canvas_bottom.pack()

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()


root = Tk()
app = Application(master=root)
app.mainloop()
