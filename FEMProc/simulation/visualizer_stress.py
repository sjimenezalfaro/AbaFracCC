from odbAccess import openOdb, ELEMENT_NODAL
import numpy as np

nombre_odb = "SteelD0_D1_l0.odb"
odb = openOdb(path=nombre_odb)

step = odb.steps['Step-1']
last_frame = step.frames[-1]


stress_field = last_frame.fieldOutputs['S']
stress_nodal = stress_field.getSubset(position=ELEMENT_NODAL)

instance = odb.rootAssembly.instances.values()[0]

tol = 1e-5  
nodos_x0 = {}

for node in instance.nodes:
    x = node.coordinates[0]
    y = node.coordinates[1]
    if abs(x) < tol:
        nodos_x0[node.label] = y

s22_dict = {}

for val in stress_nodal.values:
    if val.nodeLabel in nodos_x0:
        s22_val = val.data[0]  
        node_label = val.nodeLabel
        
        if node_label not in s22_dict:
            s22_dict[node_label] = []
        s22_dict[node_label].append(s22_val)

datos = []
for node_label, y_coord in nodos_x0.items():
    if node_label in s22_dict:
        s22_promedio = np.mean(s22_dict[node_label])
        datos.append([y_coord, s22_promedio])

datos = np.array(datos)
if len(datos) > 0:
    datos = datos[datos[:, 0].argsort()]
    
    arc_length = datos[:, 0] - datos[0, 0]
    datos[:, 0] = arc_length

np.savetxt('stress_SteelD0_D1.dat', datos, fmt='%.6e')

odb.close()