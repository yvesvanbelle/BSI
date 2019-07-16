# Licensed under the MIT license
# Copyright (c) 2016 Yves Van Belle (yvanbelle@brother.be)

import os
import glob
import shutil

def move_files(directory):
    pwd = os.getcwd()
    os.chdir(directory)
    files = glob.glob('*.pdf')
    for file in files:
        directory_name = file[ : file.index('_')]

        if not (os.path.exists(directory_name)):
            os.mkdir(directory_name)

        shutil.move(file , directory_name + os.sep + file)

    os.chdir(pwd)

if __name__ == '__main__':
    workdir = self.scandir = os.path.expanduser("~")
    move_files(workdir)
