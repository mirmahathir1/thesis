from os import listdir
from os.path import isfile, join
import shutil
import os

def get_file_list_directory(directory_path, file_ext):
    file_list = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]
    file_list = [a.split('.')[0] for a in file_list if file_ext in a]
    return file_list

def exists(path):
    return isfile(path)

def clear_temp():
    shutil.rmtree('.\\tmp', ignore_errors=True)
    os.makedirs('.\\tmp', exist_ok=True)
