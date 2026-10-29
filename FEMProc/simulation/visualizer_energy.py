from odbAccess import openOdb
from abaqusConstants import *
import numpy as np
# Open the Odb file
num_seam=42
allse_vector = []
indices = np.linspace(start=0, stop=num_seam, num=num_seam)
for ind in indices:
    
    indice_limpio = str(int(ind)).strip().replace('.', '_')
    nombre_odb = "steelD0_D1_l{}.odb".format(indice_limpio)
    odb = openOdb(path=nombre_odb)
    outstep = odb.steps['Step-1'] 

    history_region = outstep.historyRegions['Assembly ASSEMBLY']
    datos_allse = history_region.historyOutputs['ALLSE'].data
    ultimo_tiempo, ultimo_allse = datos_allse[-1]
    allse_vector.append(ultimo_allse)

allse_vector = np.array(allse_vector).reshape(-1, 1) 
np.savetxt('energy_SteelD0_D1.dat', allse_vector)