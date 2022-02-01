import os
def create_folders_list(folders_list):
    for curr in folders_list:
        try:
            os.makedirs(curr)
        except FileExistsError:
            pass

def create_folder_dirr(folder_dir,start_creat='project'):
    new_dir=folder_dir[:folder_dir.rfind(start_creat)]+start_creat
    for curr in folder_dir[folder_dir.rfind(start_creat):].split('/')[1:]:
        if curr == '': continue
        new_dir=new_dir+'/'+curr
        try:
            os.makedirs(new_dir)
        except FileExistsError:
            pass
