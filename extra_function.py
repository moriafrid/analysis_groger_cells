import os
from neuron import h,gui
def create_folders_list(folders_list):
    for curr in folders_list:
        try:
            os.makedirs(curr)
        except FileExistsError:
            pass

def create_folder_dirr(folder_dir):
    new_dir=folder_dir.split('/')[0]
    for curr in folder_dir.split('/')[1:]:
        if curr == '': continue
        new_dir=new_dir+'/'+curr
        try:
            os.makedirs(new_dir)
        except FileExistsError:
            pass
    return folder_dir+'/'

def SIGSEGV_signal_arises(signalNum, stack):
    print(f"{signalNum} : SIGSEGV arises")
    # Your code


class Cell:
    pass
    def start(self):
        self.change_to_lists()

    def delete_axon(self):
        for sec in self.axon:
            h.delete_section(sec=sec)
        self.axon = []

    def change_to_lists(self):
        self.dend = list(self.dend)
        try:
            self.apic=list(self.apic)
        except:
            self.apic=[]
        try:
            self.axon=list(self.axon)
        except:
            self.axon=[]
        if not len(self.soma)<=1:
            self.dend += [h.soma[i] for i in range(1, len(h.soma),1)]
        self.soma=self.soma[0]
        self.insert_sec=[]

    def add_sec(self,sec):
        self.insert_sec.append(sec)
    def add_axon(self,new_axon):
        self.axon.append(new_axon)
    def all_sec(self):
        return [self.soma]+self.apic+self.dend+self.axon+self.insert_sec

    def __del__(self):
        for sec in self.all_sec():
            h.delete_section(sec=sec)
        self.dend = []
        self.apic = []
        self.axon =[]
        self.insert_sec=[]

def load_ASC(ASC_dir,delete_axon=True):
    h.load_file("import3d.hoc")
    h.load_file("nrngui.hoc")
    h.load_file('stdlib.hoc')
    h.load_file("stdgui.hoc")
    #def to read ACS file
    h('objref cell, tobj')
    # h('create dend, apic, axon, soma')
    loader = h.Import3d_GUI(None)
    loader.box.unmap()
    loader.readfile(ASC_dir)
    cell = Cell()
    loader.instantiate(cell)
    cell.change_to_lists()
    if delete_axon:
        cell.delete_axon()
    return cell



class hoc_cell:
    def __init__(self, hoc_dir):
        h.load_file(1, hoc_dir)
        try:
            self.dend = list(h.dend) + [h.soma[i] for i in range(1, len(h.soma),1)]
            self.soma = h.soma[0]
        except:
            self.dend = list(h.dend)
            self.soma = h.soma
        try:
            self.axon = list(h.axon)
        except:
            print('no axon in this cell')
            self.axon=[]
        try:
            self.apic = list(h.apic)
        except:
            self.apic=[]
            print('no apical dendrite in this cell')
        self.insert_sec=[]

    def add_sec(self,sec):
        self.insert_sec.append(sec)
    def add_axon(self,new_axon):
        self.axon.append(new_axon)
    def all_sec(self):
        return [self.soma]+self.apic+self.dend+self.axon+self.insert_sec

    def delete_axon(self):
        for sec in self.axon:
            h.delete_section(sec=sec)
        self.axon = []

    def __del__(self):
        for sec in self.all_sec():
            h.delete_section(sec=sec)
        self.dend = []
        self.apic = []
        self.axon =[]
        self.insert_sec=[]

def load_hoc(hoc_dir,delete_axon=True):
    cell=hoc_cell(hoc_dir)
    if delete_axon:
        cell.delete_axon()
    return cell
def instantiate_swc(filename):
    h.load_file('import3d.hoc')
    h('objref cell, tobj')
    h.load_file('allen_model.hoc')
    h.execute('cell = new allen_model()')
    h.load_file(filename)
    nl = h.Import3d_SWC_read()
    nl.quiet = 1
    nl.input(filename)
    i3d = h.Import3d_GUI(nl, 0)
    i3d.instantiate(h.cell)
    return h.cell
# def instantiate_swc(filename):
#     h.load_file('import3d.hoc')
#     h('objref cell, tobj')
#     h.load_file('allen_model.hoc') # why using allen model.hoc?
#     h.execute('cell = new allen_model()')
#     h.load_file(filename)
#     nl = h.Import3d_SWC_read()
#     nl.quiet = 1
#     nl.input(filename)
#     i3d = h.Import3d_GUI(nl, 0)
#     i3d.instantiate(h.cell)
    # try:
    #     for sec in h.cell.axon:
    #         h.delete_section(sec=sec)
    # except:
    #     print(filename.split('/')[-1] +' dont have axon inside')
    return h.cell
class swc_cell:
    def __init__(self, swc_dir):
        self.cell=instantiate_swc(swc_dir)
        self.dend = list(self.cell.dend)
        self.soma = self.cell.soma[0]
        if len(self.cell.axon)>1:
            self.axon = list(self.cell.axon)
        else:
            print('no axon in this cell')
            self.axon=[]
        if len(self.cell.apic)>1:
            self.apic = list(self.cell.apic)
        else:
            self.apic=[]
            print('no apical dendrite in this cell')
        self.insert_sec=[]

    def add_sec(self,sec):
        self.insert_sec.append(sec)
    def add_axon(self,new_axon):
        self.axon.append(new_axon)
    def all_sec(self):
        return [self.soma]+self.apic+self.dend+self.axon+self.insert_sec

    def delete_axon(self):
        for sec in self.axon:
            h.delete_section(sec=sec)
        self.axon = []

    def __del__(self):
        for sec in self.all_sec():
            h.delete_section(sec=sec)
        self.dend = []
        self.apic = []
        self.axon =[]
        self.insert_sec=[]
def load_swc(swc_dir,delete_axon=True):
    cell=swc_cell(swc_dir)
    if delete_axon:
        cell.delete_axon()
    return cell

if __name__=='__main__':
    from open_pickle import read_from_pickle
    from glob import glob
    cell_name=read_from_pickle('cells_name.p')
    cell=None
    swc_dir=glob('cells_initial_information/'+cell_name[2]+'/*swc')[0]
    cell=load_swc(swc_dir)
    a=1

