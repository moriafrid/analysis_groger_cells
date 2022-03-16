from open_pickle import read_from_pickle
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

file_type='z_correct.swc'
plt.close('all')
for cell_name in read_from_pickle('cells_name.p'):
    plt.title(cell_name)
    #cell morphology and properties:
    
    #cells best result for passivr parameters:

    #cells result for AMPA and NMDA leakness
    plt.show()

plt.close('all')
folder='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data/'
cell_name=read_from_pickle('cells_name.p')[1]
for i in [10,20,60]:
    plt.figure()
    plt.title(cell_name+'z_correct.swc_SPINE_START='+str(i))
    dir=(folder+cell_name+'/fit_short_pulse/z_correct.swc_SPINE_START='+str(i)+'/dend*1.0&F_shrinkage=1.0/const*/RA/analysis/diffrent RA against error.png')
    img = mpimg.imread(dir)
    imgplot = plt.imshow(img)
plt.show()
