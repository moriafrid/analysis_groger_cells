class Syn2Clear:
    def __init__(self,cell_name):
        if cell_name == "2017_05_08_A_4-5":
            self.not_sure=[12,20,26,28,47,48,49,70,71,74,78,81,85,88]
            self.cut_on_1000=[8,19,21,34,35,38,40,47,48,77,81,90]
            self.rigth=[0,1,2,3,4,5,6,9,10,14,18,21,22,23,24,25,26,27,33,35,36,37,41,43,44,45,47,48,50,51,53,55,56,58,59,62,65,66,67,72,73,74,75,76,78,79,82,86] #for time2syn+1000 and stable antil point 1200
            self.false=[7,11,13,15,16,17,29,39,42,46,49,52,54,57,60,61,63,64,68,69,71,80,83,84,85,87,88,89,91]#for time2syn+1000 and stable antil point 1200
            self.remove=[11,19,24,]
        if cell_name == "2017_05_08_A_5-4":
            self.not_sure=[]
            self.cut_on_1000=[]
            self.rigth=[] #for time2syn+1000 and stable antil point 1200
            self.false=[]#for time2syn+1000 and stable antil point 1200
            self.remove=[]
        if cell_name == "2017_03_04_A_6-7":
            self.not_sure=[]
            self.cut_on_1000=[]
            self.rigth=[] #for time2syn+1000 and stable antil point 1200
            self.false=[]#for time2syn+1000 and stable antil point 1200
            self.remove=[]
