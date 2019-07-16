# Licensed under the MIT license
# Copyright (c) 2016 Yves Van Belle (yvanbelle@brother.be)


from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os
import sys
import socket


def ftp_server(ftpsrv_ip, ftpsrv_dir):
    print(r'Starting FTP server: ftp://' + ftpsrv_ip + r':2121')
    print('FTP directory is: ' + ftpsrv_dir + '\n')
    authorizer = DummyAuthorizer()
    authorizer.add_user('user', '12345', ftpsrv_dir, perm="elradfmw")
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer(('0.0.0.0', 2121), handler)
    server.serve_forever()

if __name__ == "__main__":
    ftpserver_ip = sys.argv[1]
    ftpserver_dir = sys.argv[2]

    # Check if IP address of FTP server exists
    try:
        socket.gethostbyaddr(ftpserver_ip)
    except socket.herror:
        ftpserver_ip = socket.gethostbyname(socket.gethostname())

    # Check if the directory where the FTP server writes exists
    if os.path.isdir(ftpserver_dir) == False:
        os.makedirs(ftpserver_dir)

    ftp_server(ftpserver_ip, ftpserver_dir)
