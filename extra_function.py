import os
from neuron import h
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

def SIGSEGV_signal_arises(signalNum, stack):
    print(f"{signalNum} : SIGSEGV arises")
    # Your code

class Cell: pass
def mkcell(fname):
    #def to read ACS file
    h('objref cell, tobj')
    loader = h.Import3d_GUI(None)
    loader.box.unmap()
    loader.readfile(fname)
    c = Cell()
    loader.instantiate(c)
    return c

# h.load_file('cell_path'+".hoc")
