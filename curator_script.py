# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 20:08:18 2022

@author: Nathan Turriff
"""

import os
import time
from datetime import datetime
import xlwings as xw

# place filepath in targ var

targ = r'root'

class fileData:
    def _init_(self, f_name, file_path, create_time, last_mod, last_access, 
               file_size, folder):
        self.f_name = f_name
        self.file_path = file_path
        self.create_time = create_time
        self.last_mod = last_mod
        self.last_access =  last_access
        self.file_size = file_size
        self.folder = folder
        
class folderData:
    def _init_(self, folder_name, num_files, num_folders, last_file_mod, 
               last_file_acc, folder_path, file_list):
        self.folder_name = folder_name
        self.num_files = num_files
        self.num_folders = num_folders
        self.last_file_mod = last_file_mod
        self.last_file_acc = last_file_acc
        self.folder_path = folder_path
        self.file_list = file_list
        
file_array = []
folder_array = []
same_name_size_ = []

for root, dirs, files in os.walk(targ):
    root_folder = folderData()
    root_folder.folder_name = root
    root_folder.folder_path = root
    root_folder.last_file_mod = datetime(1900,1,1)
    root_folder.last_file_acc = datetime(1900,1,1)
    root_folder.num_files = 0
    folder_array.append(root_folder)
    for name in dirs:
        fold_path = os.path.join(root, name)
        for i in folder_array:
            if (i.folder_path == fold_path): 
                print(name)
                i.folder_name = name
    for name in files:
        full_path = os.path.join(root, name)        
        path_stats = os.stat(full_path)
        creation_time = path_stats.st_ctime
        mod_time = path_stats.st_mtime
        access_time = path_stats.st_atime
        target_file = fileData()        
        target_file.folder = root
        target_file.f_name = name
        target_file.file_path =  full_path
        target_file.create_time = time.ctime(creation_time)
        target_file.last_mod = time.ctime(mod_time)
        target_file.last_access = time.ctime(access_time)
        target_file.file_size = path_stats.st_size
        file_array.append(target_file)

wb = xw.Book()

for i in file_array:
    # print(i.f_name+ "--- " + str(i.file_size))
    file_folder = i.folder
    for j in folder_array:
        folder_folder = j.folder_path
        if file_folder == folder_folder:
            j.num_files  = j.num_files + 1
            mod_date = datetime.strptime(i.last_mod, "%a %b %d %H:%M:%S %Y")
            if mod_date > j.last_file_mod :
                j.last_file_mod =  mod_date
                print(j.folder_path + ": " + str(j.last_file_mod))
            acc_date = datetime.strptime(i.last_access, "%a %b %d %H:%M:%S %Y")
            j.last_file_acc =  acc_date if acc_date > j.last_file_acc else  j.last_file_acc
            # print(j.folder_path + ": " + str(j.num_files) + " "+ str(mod_date)) 
            continue
            
    
for i in folder_array:
    print (i.folder_path + "--- \n" + str(i.last_file_mod))        