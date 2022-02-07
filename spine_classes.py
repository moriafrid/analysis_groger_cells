from math import pi,sqrt

def get_n_spinese(cell_name):
    if cell_name == "2017_03_04_A_6-7":
        return 2
    if cell_name == "2017_05_08_A_4-5":
        return 1
    if cell_name == "2017_05_08_A_5-4":
        return 2

def channel2take(cell_name,type,pre_post=None):
    if type=="electopysio":
        if pre_post is None:
            raise "need to take pre_post to be 'pre' for presynaptic neuron or 'post for postsynaptic b=neuron"
        if cell_name == "2017_03_04_A_6-7":
            pre='1'
            post='2'
        elif cell_name == "2017_05_08_A_4-5":
            pre='2'
            post='1'
        elif cell_name == "2017_05_08_A_5-4":
            pre='1'
            post='2'
        if pre_post=='pre':
            return pre
        elif pre_post=='post':
            return post
    if type=="IV_curve":
        if cell_name == "2017_03_04_A_6-7":
            return 2
        elif cell_name == "2017_05_08_A_4-5":
            return 1
        elif cell_name == "2017_05_08_A_5-4":
            return 2
    else:
        raise "this isn't correct channels"

class SpinesParams:
    def __init__(self, cell_name,spine_num=5):
        self.cell_name=cell_name
        if cell_name == "2017_05_08_A_4-5":
            self.V_spine=0.16884774101 #[µm^3]
            self.V_head=0.13906972096 #4/3*pi*self.R_head**3
            self.v_neck=0.02977802005
            self.neck_length = 0.782 #µm
            self.neck_diam = 0.164 #µm
            self.R_head = (self.V_spine/(4*pi/3))**(1/3) #0.32µm
            self.head_diam=2*self.R_head #µm 0.64
            self.PSD_area=0.14
        if cell_name == "2017_05_08_A_5-4":
            if spine_num==0:
                self.V_spine=0.06818310193 #[µm^3]
                self.V_head=0.03371715503 #[µm^3] #4/3*pi*self.R_head**3
                self.v_neck=0.0344659469 #[µm^3]
                self.neck_length = 1.266 #µm
                self.neck_diam =0.125 #µm
                self.R_head = (self.V_spine/(4*pi/3))**(1/3) #µm
                self.head_diam=2*self.R_head #µm
                self.PSD_area=0.066
            elif spine_num==1:
                self.V_spine=0.02865474235 #[µm^3]
                self.V_head=0.01125841287 #[µm^3] #4/3*pi*self.R_head**3
                self.v_neck=0.01739632948 #[µm^3]
                self.neck_length = 1.121 #µm
                self.neck_diam =0.102 #µm
                self.R_head = (self.V_spine/(4*pi/3))**(1/3) #µm
                self.head_diam=2*self.R_head #µm
                self.PSD_area=0.014
            else: raise "there is more than one synapse"

        if cell_name == "2017_03_04_A_6-7":
            if spine_num==0:
                self.V_spine=0.08501695029 #[µm^3]
                self.V_head=0.0745871871 #[µm^3] #4/3*pi*self.R_head**3
                self.v_neck=0.01042976319 #[µm^3]

                self.neck_length = 0.763 #µm
                self.neck_diam =0.134 #µm

                self.R_head = (self.V_spine/(4*pi/3))**(1/3) #µm
                self.head_diam=2*self.R_head #µm
                self.PSD_area=0.114
            elif spine_num==1:
                self.V_spine=0.0783942101 #[µm^3]
                self.V_head=0.06459193692 #[µm^3] #4/3*pi*self.R_head**3
                self.v_neck=0.01380227318 #[µm^3]

                self.neck_length = 0.905 #µm
                self.neck_diam =0.039 #µm

                self.R_head = (self.V_spine/(4*pi/3))**(1/3) #µm
                self.head_diam=2*self.R_head #µm
                self.PSD_area=0.039
            else: raise "there is more than one synapse"

    def get_F_factor_params(self):
        return self.R_head,self.neck_diam,self.neck_length


class GeneralSpine:
    def __init__(self, cell_type):
        if cell_type=="mouse_spine":
            #mouse https://link.springer.com/content/pdf/10.1023/A:1024134312173.pdf
            self.head_area=0.37
            self.R_head=sqrt(self.head_area/(4*pi))
            self.neck_length=0.73
            self.head_diam=2*self.R_head
            self.neck_diam=0.25 #0.164/07=0.23
            self.spine_density=1.08
            self.V_head=4/3*pi*self.R_head**3
        elif cell_type== "shaft_spine":
            self.neck_length=0.001
            self.head_diam=0.944
            self.R_head=self.head_diam/2
            self.V_head=4/3*pi*self.R_head**3
        elif cell_type== "human_spine":
            self.neck_length=1.35
            self.head_diam=0.944
            self.R_head=self.head_diam/2
            self.V_head=4/3*pi*self.R_head**3
        else: raise "this isn't exceptable spine type"
    def get_F_factor_params(self):
        return self.R_head,self.neck_diam,self.neck_length

class SpineLocatin:
    def __init__(self, cell_name,spine_num=5):
        if cell_name == "2017_05_08_A_4-5":
            self.dis_from_soma=83.8
            self.locatin_xyz=() #need to be change
            self.sec=82
            self.seg=0.165
            self.PSD=0.14
        if cell_name == "2017_05_08_A_5-4":
            if spine_num==0:
                self.dis_from_soma=77.5
                self.locatin_xyz=() #need to be change
                self.sec=1 #need to be change
                self.seg=0.1 #need to be change
                self.PSD=0.066
            elif spine_num==1:
                self.dis_from_soma=74.3
                self.locatin_xyz=() #need to be change
                self.sec=1 #need to be change
                self.seg=0.1 #need to be change
                self.PSD=0.014
            else: raise "there is more than one synapse"
        if cell_name == "2017_03_04_A_6-7":
            if spine_num==0:
                self.dis_from_soma=32.6
                self.locatin_xyz=() #need to be change
                self.sec=1 #need to be change
                self.seg=0.1 #need to be change
                self.PSD=0.144
            elif spine_num==1:
                self.dis_from_soma=50.6
                self.locatin_xyz=() #need to be change
                self.sec=1 #need to be change
                self.seg=0.1 #need to be change
                self.PSD=0.039
            else: raise "there is more than one synapse"





if __name__ == '__main__':
    spine=SpinesParams("2017_05_08_A_4-5")
