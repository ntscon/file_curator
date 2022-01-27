# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 20:08:18 2022

@author: Nathan Turriff
"""

import os
import time

# place filepath in targ var

targ = r'root'

class fileData:
    def _init_(self, f_name, file_path, last_mod, last_access, 
               file_size, folder):
        self.f_name = f_name
        self.file_path = file_path
        self.last_mod = last_mod
        self.last_access =  last_access
        self.file_size = file_size
        self.folder = folder
        
class folderData:
    def _init_(self, folder_name, num_files, num_folders, last_file_mod, 
               last_child_mod, folder_path, file_list):
        self.folder_name = folder_name
        self.num_files = num_files
        self.num_folders = num_folders
        self.last_file_mod = last_file_mod
        self.last_child_mod = last_child_mod
        self.folder_path = folder_path
        self.file_list = file_list
        
file_array = []
folder_array = []

for root, dirs, files in os.walk(targ):
    for name in dirs:
        direct = folderData()
        direct.folder_name = name
        fold_path = os.path.join(root, name)
        file_list = [f for f in os.listdir('.') if os.path.isfile(f)]
        direct.file_list = file_list
        direct.num_files = len(file_list)
        folder_array.append(direct)
    
    for name in files:
        full_path = os.path.join(root, name)        
        path_stats = os.stat(full_path)
        mod_time = path_stats.st_mtime
        access_time = path_stats.st_atime
        target_file = fileData()        
        target_file.folder = root
        target_file.f_name = name
        target_file.file_path =  full_path
        target_file.last_mod = time.ctime(mod_time)
        target_file.last_access = time.ctime(access_time)
        target_file.file_size = path_stats.st_size
        file_array.append(target_file)


for i in file_array:
    print(i.folder+ "--- " + str(i.file_size))
    
# for i in folder_array:
#     print (i.folder_name + "--- " + str(i.num_files) + "--- " )        