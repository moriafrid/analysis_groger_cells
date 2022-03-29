import cv2
import matplotlib.pyplot as plt
from glob import glob
from analysis_fit_after_run import analysis_fit

for cell_name in ["2017_05_08_A_5-4", "2017_05_08_A_4-5","2017_03_04_A_6-7"]:
    for folder in glob('/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data_short/'+cell_name+'/fit_short_pulse_ASC/dend*1.0&F_shrinkage=1.0/different_initial_conditions/*'):
        if folder.rfind('RA')!=folder.find('RA'): continue
        analysis_fit(folder)

    for png in glob('/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data_short/'+cell_name+'/fit_short_pulse_ASC/dend*1.0&F_shrinkage=1.0/different_initial_conditions/*/*/diffrent RA0 against error.png'):

        img=cv2.imread(png)
        plt.figure()
        plt.title(cell_name)
        plt.imshow(img)
        plt.show()

    a=1
