import os
import sys
import glob
import shutil
from datetime import datetime


current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

download_folder = "C:\\Users\\Ben\\Downloads\\test"

file_types = {
    'image': ['.jpg',
               '.jpeg',
               '.png',
    ],
    'video': ['.mp4',
               '.wmv',
               '.avi',
               '.mkv',
               '720p',
               '1080p',
               'BRRip',
               'webrip',
               'xvid'],
    'text': ['.doc',
             '.docx',
             '.odf',
             '.txt',
             '.rtf',
             '.md',
             '.pdf'],
    'archive': ['.rar',
                '.zip',
                '.7zip'],
    'executable': ['.exe',
                   '.bat',
                   '.app',
                   '.msi'],
    'presentation': ['.ppt',
                     '.pptx',
                     '.odp'],
    'spreadsheet': ['.xls',
                    '.xlsx',
                    '.ods',
                    '.csv']
}


file_destinations = {
    'image': 'C:\\Users\\Ben\\Pictures\\Downloaded Images',
    'video': 'C:\\Users\\Ben\\Videos\\Downloaded Videos',
    'text': 'C:\\Users\\Ben\\Documents\\Downloaded Documents\\Text Files',
    'archive': 'C:\\Users\\Ben\\Downloads\\Archive Files',
    'spreadsheet': 'C:\\Users\\Ben\\Documents\\Downloaded Documents\\Spreadsheets',
    'presentation': 'C:\\Users\\Ben\\Documents\\Downloaded Documents\\Presentations',
    'executable': 'C:\\Users\\Ben\\Downloads\\Executables'
}

def log_move(file, path):
    print("log move")
    with open("C:\\Users\\Ben\\Downloads\\file_move_log.txt", "a+") as logfile:
        logfile.write(current_time + ": " + path + " <-- " + str(file[23:]) + "\n")
        print("logged")

def move_file(file, filetype):
    for ftype, path in file_destinations.items():
        if filetype == ftype:
            print("move " + file + " to " + path)
            if os.path.exists(path):
                # shutil.move(file, path)
                log_move(file, path)
            else:
                # os.mkdir(path)
                # shutil.move(file, path)
                log_move(file, path)

def file_type(file):
    print("==============")
    
    file_known = "checking"
    
    for key, value in file_types.items():
        
        if any(word in file.lower() for word in value):
            file_known = "yes"
            print(file)
            print("Type: " + key)
            move_file(file, key)
                
        
    if file_known != "yes":
        
        if os.path.isdir(file):
            print(file)
            print("is directory")
        else:
            print(file)
            print("UNKNOWN")
    
def sort():
    file_count = 0
    for item in os.listdir(download_folder):
        item = str(download_folder) + "\\" + str(item)
        if "file type paths" not in item and "file_move_log" not in item:
            file_type(item)
            file_count += 1
    return file_count