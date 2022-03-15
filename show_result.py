from open_pickle import read_from_pickle
import matplotlib.pyplot as plt
file_type='z_correct.swc'
for cell_name in read_from_pickle('cells_name.p'):
    plt.title(cell_name)
    #cell morphology and properties:
    
    #cells best result for passivr parameters:

    #cells result for AMPA and NMDA leakness
    plt.show()
