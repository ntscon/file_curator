# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 20:08:18 2022

@author: Nathan Turriff
"""

import os
import time
from datetime import datetime
import xlwings as xw

defaultDate = datetime(1900,1,1)

# place filepath in targ var

targ = r'C:\Users\Nathan\Desktop\Cosa_mia'

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
    def _init_(self, folder_name, num_files, child_folders, last_file_mod, 
               last_file_acc, folder_path, file_list, all_cut):
        self.folder_name = folder_name
        self.num_files = num_files
        self.child_folders = child_folders
        self.last_file_mod = last_file_mod
        self.last_file_acc = last_file_acc
        self.folder_path = folder_path
        self.file_list = file_list
        self.all_cut = all_cut
        
file_array = []
folder_array = []
same_name_size_ = []

for root, dirs, files in os.walk(targ):
    root_folder = folderData()
    root_folder.folder_name = root
    root_folder.folder_path = root
    root_folder.child_folders = dirs
    root_folder.last_file_mod = defaultDate
    root_folder.last_file_acc = defaultDate
    root_folder.num_files = 0
    folder_array.append(root_folder)
    for name in dirs:
        fold_path = os.path.join(root, name)
        for i in folder_array:
            if (i.folder_path == fold_path): 
                i.folder_name = name
                
    for name in files:
        full_path = os.path.join(root, name)
        target_file = fileData()         
        target_file.file_path =  full_path
        target_file.last_mod = defaultDate
        target_file.last_access = defaultDate
        try: 
            path_stats = os.stat(full_path)
            creation_time = path_stats.st_ctime
            mod_time = path_stats.st_mtime
            access_time = path_stats.st_atime       
            target_file.folder = root
            target_file.f_name = name
            target_file.file_path =  full_path
            target_file.create_time = time.ctime(creation_time)
            target_file.last_mod = time.ctime(mod_time)
            target_file.last_access = time.ctime(access_time)
            target_file.file_size = path_stats.st_size
            file_array.append(target_file)
        except: continue

wb = xw.Book()
wb.save(r'C:\Users\Nathan\Desktop\Cosa_mia\1.xlsx')
folderSheet = wb.sheets.add('before cut off')
fileSheet = wb.sheets.add('duplicate files')
        
cutOffDate = datetime(2020,8,1)

for i in file_array:
    file_folder = i.folder
    for j in folder_array:
        folder_folder = j.folder_path
        if file_folder == folder_folder:
            j.num_files  = j.num_files + 1
            mod_date = datetime.strptime(i.last_mod, "%a %b %d %H:%M:%S %Y")
            if mod_date > j.last_file_mod :
                j.last_file_mod =  mod_date
            acc_date = datetime.strptime(i.last_access, "%a %b %d %H:%M:%S %Y")
            j.last_file_acc =  acc_date if acc_date > j.last_file_acc else j.last_file_acc
            continue
            

currCount = 2

folder_array_length = len(folder_array)

for i, file in enumerate(reversed(folder_array)):
    file.all_cut = False
    if (file.last_file_mod < cutOffDate and file.last_file_mod != defaultDate):
        if (not file.child_folders):
            file.all_cut = True
        else:
            file.all_cut = True
            for child_f in file.child_folders:
                if file.all_cut == False:
                    continue
                full_child = os.path.join(file.folder_path, child_f) 
                for j in range(1,i+1):
                    examine = folder_array_length - j
                    if (folder_array[examine].folder_path == full_child):
                        aaaaa = folder_array[examine]
                        if (folder_array[examine].all_cut == False):
                            file.all_cut = False
                            continue

        if file.child_folders and file.all_cut:
            folderSheet.range(currCount, 2).value = "True"
        if file.child_folders:
            folderSheet.range(currCount, 4).value = str(file.child_folders)
        folderSheet.range(currCount, 3).value = file.folder_path
        folderSheet.range(currCount, 1).value = file.last_file_mod

        currCount = currCount + 1

        
        
stopPoint = len(file_array)

dupPaths = []

currCount = 2

for i, file in enumerate(file_array):
    focMod = file.last_mod
    focName = file.f_name
    focSize = file.file_size
    focFolder = file.folder
    focFP = file.file_path
    for j in range(i, stopPoint):
        susFile = file_array[j]
        if susFile.file_size == focSize and susFile.folder != focFolder \
            and dupPaths.count(susFile.file_path) < 1:
            if (susFile.last_mod == focMod and susFile.f_name == focName):
                fileSheet.range(currCount, 2).value =  focName
                fileSheet.range(currCount, 3).value =  susFile.file_path
                fileSheet.range(currCount, 4).value =  focFP
                currCount = currCount + 1
                print("likely duplicate: " + "\n   " + susFile.file_path +
                      "\n   " + focFP)
                dupPaths.append(susFile.file_path)