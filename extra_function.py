import os
from neuron import h,gui
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
    h.load_file("import3d.hoc")
    h.load_file("nrngui.hoc")
    h.load_file('stdlib.hoc')
    h.load_file("stdgui.hoc")
    #def to read ACS file
    h('objref cell, tobj')
    loader = h.Import3d_GUI(None)
    loader.box.unmap()
    loader.readfile(fname)
    cell = Cell()
    loader.instantiate(cell)
    return cell

def instantiate_swc(filename):
    h.load_file('import3d.hoc')
    h('objref cell, tobj')
    h.load_file('allen_model.hoc') # why using allen model.hoc?
    h.execute('cell = new allen_model()')
    h.load_file(filename)
    nl = h.Import3d_SWC_read()
    nl.quiet = 1
    nl.input(filename)
    i3d = h.Import3d_GUI(nl, 0)
    i3d.instantiate(h.cell)
    try:
        for sec in h.cell.axon:
            h.delete_section(sec=sec)
    except:
        print(filename.split('/')[-1] +' dont have axon inside')
    return h.cell

class hoc_cell:
    def __init__(self, hoc_dir):
        h.load_file(hoc_dir)
        self.dend = h.dend
        self.apic = h.apic
        self.soma = h.soma
        try:
            self.axon = h.axon
        except:
            print('no axon in this cell')

def load_hoc(hoc_dir):
    return hoc_cell(hoc_dir)


