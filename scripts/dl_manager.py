import os
import sys
import glob
import shutil
from datetime import datetime


current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

download_folder = "C:\\Users\\Ben\\Downloads"

file_types = {
    'image': ['.jpg',
               '.jpeg',
               '.png',
               '.jpe'
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
             '.pdf',
             '.azw',
             '.azw3',
             '.epub'],
    'archive': ['.rar',
                '.zip',
                '.7zip',
                '.7z',
                '.iso'],
    'executable': ['.exe',
                   '.bat',
                   '.app',
                   '.msi',
                   '.bin',
                   '.ico'],
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
    'executable': 'C:\\Users\\Ben\\Downloads\\Executables',
    'unknown': 'C:\\Users\\Ben\\Downloads\\Unknown Files',
}

def log_move(file, path):
    print("log move")
    with open("C:\\Users\\Ben\\Downloads\\file_move_log.txt", "a+") as logfile:
        logfile.write(current_time + ": " + str(file[23:]) + " --> " + path + "\n")
        print("logged")

def move_file(file, filetype):
    for ftype, path in file_destinations.items():
        if filetype == ftype:
            print("move " + file + " to " + path)
            if os.path.exists(path):
                try:
                    shutil.move(file, path)
                    log_move(file, path)
                    return "success"
                except:
                    print(file + " already exists in " + path)
                    return "failed"
            else:
                os.mkdir(path)
                try:
                    shutil.move(file, path)
                    log_move(file, path)
                    return "success"
                except:
                    print(file + " already exists in " + path)
                    return "failed"

def file_type(file):
    print("==============")
    
    file_known = "checking"
    
    for key, value in file_types.items():
        
        if any(word in file.lower() for word in value):
            file_known = "yes"
            print(file)
            print("Type: " + key)
            if move_file(file, key) == "success":
                return "moved"
                
        
    if file_known != "yes":
        # check if the download is a directory
        if os.path.isdir(file):
            print(file)
            print("is directory")
            
            par1 = "("
            par2 = ")"
            # check if the directory is a movie directory (as they sometimes come in folders with the year in brackets)
            if par1 in file:
                print("FILM FOLDER")
                year = file[file.find(par1)+1 : file.find(par2)]
                print(year)
                if int(year):
                    if move_file(file, "video") == "success":
                        return "moved"
                           
        else:
            print(file)
            print("UNKNOWN")
            if move_file(file, "unknown") == "success":
                return "moved"
    return "not moved"
    
def sort():
    file_count = 0
    for item in os.listdir(download_folder):
        item = str(download_folder) + "\\" + str(item)
        if "file type paths" not in item and "file_move_log" not in item:
            if file_type(item) == "moved": # we only want to update the count if we actually moved the file/folder
                file_count += 1
    return file_count