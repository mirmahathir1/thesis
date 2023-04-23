from os import listdir
from os.path import isfile, join
import shutil
import os

def get_file_list_directory(directory_path, file_ext):
    file_list = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]
    file_list = [a.replace(file_ext,'') for a in file_list if file_ext in a]
    return file_list

def get_file_list_directory_recurse(director_path, file_ext):
    final_list_of_files = []
    for root, dirs, files in os.walk(director_path):
        for file in files:
            if file.endswith(file_ext):
                final_list_of_files.append(os.path.join(root, file))
    return final_list_of_files

def get_folder_list_directory(directory_path):
    return [name for name in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, name))]

def exists(path):
    return isfile(path)

def clear_temp():
    shutil.rmtree('.\\tmp', ignore_errors=True)
    os.makedirs('.\\tmp', exist_ok=True)

def move(source, destination):
    shutil.move(source, destination) 

def makedir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def read_lines_from_file_object(fileObject):
    return [line.strip() for line in fileObject.readlines()]
