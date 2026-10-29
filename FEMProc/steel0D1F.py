from abaqus import *
from abaqusConstants import *
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import numpy as np
import os
# ==============================================================================
# INITIAL DATA
# ==============================================================================
Lmitad = 42
Lamitad = 40
Hmitad = 10
Diam = 1.69
Rad = Diam / 2
htot = 9.27
num_particiones = 60    # Number of total partitions along the expected crack path
bias = 0.1              # Factor de crecimiento (<1 para agrandar al final)
num_seam=num_particiones
indices = np.linspace(start=0, stop=num_particiones, num=num_particiones)
# Abaqus directory
os.chdir("./simulation")
for i in indices:
    ind_i = int(i)
    if 'mdb' in globals() or 'mdb' in locals():
        mdb.close()
    Mdb()
    session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)

    ruta = "edition/steel0_D1F_l{}.cae".format(ind_i)
    mdb.saveAs(pathName=ruta)
    # ==============================================================================
    # PART BASE
    # ==============================================================================
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=100.0)
    mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-Lmitad, -Hmitad), 
        point2=(Lmitad, Hmitad))
    mdb.models['Model-1'].Part(dimensionality=TWO_D_PLANAR, name='Part', type=
        DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['Part'].BaseShell(sketch=
        mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']
    mdb.models['Model-1'].ConstrainedSketch(gridSpacing=4.31, name='__profile__', 
        sheetSize=172.69, transform=
        mdb.models['Model-1'].parts['Part'].MakeSketchTransform(
        sketchPlane=mdb.models['Model-1'].parts['Part'].faces[0], 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 0.01258, 
        0.0)))
    mdb.models['Model-1'].parts['Part'].projectReferencesOntoSketch(filter=COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__profile__'])
    # ==============================================================================
    # NOTCH
    # ==============================================================================
    mdb.models['Model-1'].ConstrainedSketch(gridSpacing=4.31, name='__profile__', sheetSize=172.69)
    mdb.models['Model-1'].parts['Part'].projectReferencesOntoSketch(filter=COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__profile__'])
    mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-Rad, -Hmitad), point2=(Rad, -(Hmitad-htot+Rad)))
    mdb.models['Model-1'].parts['Part'].Cut(sketch=mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']
    mdb.models['Model-1'].ConstrainedSketch(gridSpacing=4.51, name='__profile__', sheetSize=180.48)
    mdb.models['Model-1'].parts['Part'].projectReferencesOntoSketch(filter=COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__profile__'])
    mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(0.0, -(Hmitad-htot+Rad)), point1=(-Rad, -(Hmitad-htot+Rad)))
    mdb.models['Model-1'].parts['Part'].Cut(sketch=mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']
    # ==============================================================================
    # PARTITIONS
    # ==============================================================================
    mdb.models['Model-1'].ConstrainedSketch(gridSpacing=4.31, name='__profile__', 
        sheetSize=172.69, transform=
        mdb.models['Model-1'].parts['Part'].MakeSketchTransform(
        sketchPlane=mdb.models['Model-1'].parts['Part'].faces[0], 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 0.01258, 
        0.0)))
    mdb.models['Model-1'].parts['Part'].projectReferencesOntoSketch(filter=
        COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__profile__'])
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0, -Hmitad), 
        point2=(0.0, Hmitad))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(-Lamitad, -Hmitad-1), 
        point2=(-Lamitad,Hmitad+1))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(Lamitad,-Hmitad-1), 
        point2=(Lamitad,Hmitad+1))
    cara_para_particionar = mdb.models['Model-1'].parts['Part'].faces.findAt(((0.0, 0.0, 0.0), ))
    mdb.models['Model-1'].parts['Part'].PartitionFaceBySketch(
        faces=cara_para_particionar, 
        sketch=mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']
    # ==============================================================================
    # SECTION, MATERIAL
    # ==============================================================================
    mdb.models['Model-1'].Material(name='Steel0')
    mdb.models['Model-1'].materials['Steel0'].Elastic(table=((168000.0, 0.3), ))
    mdb.models['Model-1'].HomogeneousSolidSection(material='Steel0', name='Section', thickness=None)
    mdb.models['Model-1'].sections['Section'].setValues(material='Steel0', thickness=10.0)
    cara_izq_extrema = mdb.models['Model-1'].parts['Part'].faces.findAt((( -Lamitad-1.0,   0.0, 0.0), ))
    cara_izq_central = mdb.models['Model-1'].parts['Part'].faces.findAt((( -Lamitad/2,   0.0, 0.0), ))
    cara_der_central = mdb.models['Model-1'].parts['Part'].faces.findAt(((  Lamitad/2,   0.0, 0.0), ))
    cara_der_extrema = mdb.models['Model-1'].parts['Part'].faces.findAt(((  Lamitad+1.0,   0.0, 0.0), ))
    mdb.models['Model-1'].parts['Part'].Set(
        faces=(cara_izq_extrema, cara_izq_central, cara_der_central, cara_der_extrema), 
        name='Set-FullGeom'
    )
    mdb.models['Model-1'].parts['Part'].SectionAssignment(offset=0.0, offsetField=
        '', offsetType=MIDDLE_SURFACE, region=
        mdb.models['Model-1'].parts['Part'].sets['Set-FullGeom'], sectionName=
        'Section', thicknessAssignment=FROM_SECTION)
    # ==============================================================================
    # ASSEMBLY, STEP
    # ==============================================================================
    mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-1', part=
        mdb.models['Model-1'].parts['Part'])
    mdb.models['Model-1'].rootAssembly.makeIndependent(instances=(
        mdb.models['Model-1'].rootAssembly.instances['Part-1'], ))
    mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')
    # ==============================================================================
    # LOADS
    # ============================================================================== 
    vertice_carga = mdb.models['Model-1'].rootAssembly.instances['Part-1'].vertices.findAt(((0.0, Hmitad, 0.0), ))
    mdb.models['Model-1'].rootAssembly.Set(vertices=vertice_carga, name='Set-Load')
    mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
        distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
        'Load', region=mdb.models['Model-1'].rootAssembly.sets['Set-Load'], u1=
        0.0, u2=-1.0, ur3=UNSET)
    # ==============================================================================
    # APPLIED DISPLACEMENT
    # ==============================================================================
    mdb.models['Model-1'].rootAssembly.regenerate()
    v_izq = mdb.models['Model-1'].rootAssembly.instances['Part-1'].vertices.findAt(((-Lamitad, -Hmitad, 0.0), ))
    v_dch = mdb.models['Model-1'].rootAssembly.instances['Part-1'].vertices.findAt(((Lamitad, -Hmitad, 0.0), ))
    mdb.models['Model-1'].rootAssembly.Set(vertices=(v_izq,v_dch), name='Set-Apoyos')
    mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
        distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
        'Apoyos', region=mdb.models['Model-1'].rootAssembly.sets['Set-Apoyos'], u1=
        UNSET, u2=0.0, ur3=UNSET)

    # ==============================================================================
    # CRACK ADVANCE
    # ==============================================================================
    y_inicio = -(Hmitad-htot)
    y_fin = Hmitad
    longitud_total = y_fin - y_inicio
   
    if bias == 1.0:
        rel_sizes = np.ones(num_particiones)
    else:
        rel_sizes = (1/bias) ** (1.0/(num_particiones-1))
        espesores = np.zeros(num_particiones)
        espesores[0] = longitud_total*(1-rel_sizes)/(1-rel_sizes**num_particiones)
        for k in range(num_particiones):
            espesores[k] = espesores[0]*rel_sizes**(k)
        
    alturas_y = np.zeros(num_particiones + 1)
    alturas_y[0] = y_inicio
    for k in range(num_particiones):
        alturas_y[k+1] = alturas_y[k] + espesores[k]
    
    t = mdb.models['Model-1'].parts['Part'].MakeSketchTransform(
        sketchPlane=mdb.models['Model-1'].parts['Part'].faces[0],
        sketchPlaneSide=SIDE1,
        sketchOrientation=RIGHT,
        origin=(0.0,0.0,0.0)
    )
    s = mdb.models['Model-1'].ConstrainedSketch(
        name='__partition__',
        sheetSize=200.0,
        transform=t
    )
    mdb.models['Model-1'].parts['Part'].projectReferencesOntoSketch(
        sketch=s,
        filter=COPLANAR_EDGES
    ) 

    x_inf = espesores[0]
    y_inf = sqrt(Rad**2-x_inf**2)+(alturas_y[0]-Rad)
    x_sup = 0.5
    y_sup = Hmitad
    s.Line(
            point1=(x_inf, y_inf),
            point2=(x_sup, y_sup)
        )
    
    s.Line(
            point1=(-x_inf, y_inf),
            point2=(-x_sup, y_sup)
        )

    for y in alturas_y[1:-1]:

        x_derecha = x_inf + (x_sup-x_inf)*(y-y_inf)/(y_sup-y_inf)

        s.Line(
            point1=(-x_derecha, float(y)),
            point2=(x_derecha, float(y))
        )
    
    s.rectangle(point1=(-2.5, -Hmitad), 
        point2=(0, -9.0))
    s.rectangle(point1=(2.5, -Hmitad), 
        point2=(0, -9.0))

    mdb.models['Model-1'].parts['Part'].PartitionFaceBySketch(
        faces=mdb.models['Model-1'].parts['Part'].faces,
        sketch=s
    )

    mdb.models['Model-1'].rootAssembly.regenerate()
       
    # ==============================================================================
    # SEAM ASSINGMENT
    # ==============================================================================
    
    if ind_i > 0:
        num_seam_i = min(ind_i, num_particiones)
        puntos_busqueda = []
        
        for k in range(num_seam_i):
            y_medio = (alturas_y[k] + alturas_y[k+1]) / 2.0
            puntos_busqueda.append(((0.0, y_medio, 0.0), ))

        aristas_seam = mdb.models['Model-1'].rootAssembly.instances['Part-1'].edges.findAt(*puntos_busqueda)
        
        mdb.models['Model-1'].rootAssembly.Set(edges=aristas_seam, name='Set-Seam-Crack')
        mdb.models['Model-1'].rootAssembly.engineeringFeatures.assignSeam(
            regions=mdb.models['Model-1'].rootAssembly.sets['Set-Seam-Crack']
        )

        mdb.models['Model-1'].rootAssembly.regenerate()

    # ==============================================================================
    # MESH SEED
    # ==============================================================================
    puntos_busqueda_total = []
    for i in range(num_particiones):
        y_medio = (alturas_y[i] + alturas_y[i+1]) / 2.0
        puntos_busqueda_total.append(((0.0, y_medio, 0.0), ))
    aristas_centrales = mdb.models['Model-1'].rootAssembly.instances['Part-1'].edges.findAt(*puntos_busqueda_total)
    mdb.models['Model-1'].rootAssembly.seedEdgeByNumber(
        edges=aristas_centrales, 
        number=1, 
        constraint=FIXED 
    )
    mdb.models['Model-1'].rootAssembly.regenerate()
    for i in range(num_particiones):
        y_medio = (alturas_y[i] + alturas_y[i+1]) / 2.0
        x_derecha = x_inf + (x_sup-x_inf)*(y_medio-y_inf)/(y_sup-y_inf)
        puntos_busqueda_total.append(((x_derecha, y_medio, 0.0), ))
    aristas_centrales = mdb.models['Model-1'].rootAssembly.instances['Part-1'].edges.findAt(*puntos_busqueda_total)
    mdb.models['Model-1'].rootAssembly.seedEdgeByNumber(
        edges=aristas_centrales, 
        number=1, 
        constraint=FIXED 
    )
    mdb.models['Model-1'].rootAssembly.regenerate()
    

    size_ext = 2.0
    todas_las_aristas = mdb.models['Model-1'].rootAssembly.instances['Part-1'].edges
    mdb.models['Model-1'].rootAssembly.seedEdgeBySize(
        edges=todas_las_aristas, 
        size=size_ext,                  
        deviationFactor=0.1, 
        constraint=FIXED            
    )

    coord_arista_infizq2 = (-Lamitad/2, -Hmitad, 0.0)
    arista_infizq2  = mdb.models['Model-1'].rootAssembly.instances['Part-1'].edges.findAt((coord_arista_infizq2, ))[0:1]
    mdb.models['Model-1'].rootAssembly.seedEdgeByBias(
        biasMethod=SINGLE, 
        end1Edges=arista_infizq2,  
        minSize=0.2,               
        maxSize=2.0,               
        constraint=FREE         
    )

    coord_arista_infcha2 = (Lamitad/2, -Hmitad, 0.0)
    arista_infcha2  = mdb.models['Model-1'].rootAssembly.instances['Part-1'].edges.findAt((coord_arista_infcha2, ))[0:1]
    mdb.models['Model-1'].rootAssembly.seedEdgeByBias(
        biasMethod=SINGLE, 
        end2Edges=arista_infcha2,  
        minSize=0.2,               
        maxSize=2.0,               
        constraint=FREE          
    )

    mdb.models['Model-1'].rootAssembly.regenerate()

    coord_arista_infizq1 = (-1.01*Rad, -Hmitad, 0.0)
    arista_infizq1  = mdb.models['Model-1'].rootAssembly.instances['Part-1'].edges.findAt((coord_arista_infizq1, ))[0:1]
    mdb.models['Model-1'].rootAssembly.seedEdgeBySize(
        edges=arista_infizq1, 
        size=0.2, 
        deviationFactor=0.1, 
        constraint=FIXED
    )

    coord_arista_infcha1 = (1.01*Rad, -Hmitad, 0.0)
    arista_infcha1  = mdb.models['Model-1'].rootAssembly.instances['Part-1'].edges.findAt((coord_arista_infcha1, ))[0:1]
    mdb.models['Model-1'].rootAssembly.seedEdgeBySize(
        edges=arista_infcha1, 
        size=0.2, 
        deviationFactor=0.1, 
        constraint=FIXED
    )

    coord_arista_infizq3 = (-1.01*Rad, -9.0, 0.0)
    arista_infizq3  = mdb.models['Model-1'].rootAssembly.instances['Part-1'].edges.findAt((coord_arista_infizq3, ))[0:1]
    mdb.models['Model-1'].rootAssembly.seedEdgeBySize(
        edges=arista_infizq3, 
        size=0.2, 
        deviationFactor=0.1, 
        constraint=FIXED
    )

    coord_arista_infcha3 = (1.01*Rad, -9.0, 0.0)
    arista_infcha3  = mdb.models['Model-1'].rootAssembly.instances['Part-1'].edges.findAt((coord_arista_infcha3, ))[0:1]
    mdb.models['Model-1'].rootAssembly.seedEdgeBySize(
        edges=arista_infcha3, 
        size=0.2, 
        deviationFactor=0.1, 
        constraint=FIXED
    )

    coord_arista_infizq4 = (-Rad, -Hmitad*0.99, 0.0)
    arista_infizq4  = mdb.models['Model-1'].rootAssembly.instances['Part-1'].edges.findAt((coord_arista_infizq4, ))[0:1]
    mdb.models['Model-1'].rootAssembly.seedEdgeBySize(
        edges=arista_infizq4, 
        size=0.2, 
        deviationFactor=0.1, 
        constraint=FIXED
    )

    coord_arista_infcha4 = (Rad, -Hmitad*0.99, 0.0)
    arista_infcha4  = mdb.models['Model-1'].rootAssembly.instances['Part-1'].edges.findAt((coord_arista_infcha4, ))[0:1]
    mdb.models['Model-1'].rootAssembly.seedEdgeBySize(
        edges=arista_infcha4, 
        size=0.2, 
        deviationFactor=0.1, 
        constraint=FIXED
    )

    coord_arista_infizq5 = (-2.5, -9.0*1.001, 0.0)
    arista_infizq5  = mdb.models['Model-1'].rootAssembly.instances['Part-1'].edges.findAt((coord_arista_infizq5, ))[0:1]
    mdb.models['Model-1'].rootAssembly.seedEdgeBySize(
        edges=arista_infizq5, 
        size=0.2, 
        deviationFactor=0.1, 
        constraint=FREE
    )

    coord_arista_infcha5 = (2.5, -9.0*1.001, 0.0)
    arista_infcha5  = mdb.models['Model-1'].rootAssembly.instances['Part-1'].edges.findAt((coord_arista_infcha5, ))[0:1]
    mdb.models['Model-1'].rootAssembly.seedEdgeBySize(
        edges=arista_infcha5, 
        size=0.2, 
        deviationFactor=0.1, 
        constraint=FREE
    )

    coord_arista_infizq6 = (-Rad, alturas_y[0]-Rad*0.999, 0.0)
    arista_infizq6  = mdb.models['Model-1'].rootAssembly.instances['Part-1'].edges.findAt((coord_arista_infizq6, ))[0:1]
    mdb.models['Model-1'].rootAssembly.seedEdgeBySize(
        edges=arista_infizq6, 
        size=0.2, 
        deviationFactor=0.1, 
        constraint=FIXED
    )

    coord_arista_infcha6 = (Rad, alturas_y[0]-Rad*0.999, 0.0)
    arista_infcha6  = mdb.models['Model-1'].rootAssembly.instances['Part-1'].edges.findAt((coord_arista_infcha6, ))[0:1]
    mdb.models['Model-1'].rootAssembly.seedEdgeBySize(
        edges=arista_infcha6, 
        size=0.2, 
        deviationFactor=0.1, 
        constraint=FIXED
    )

    from math import *
    coord_circ1 = (Rad*cos(pi/4), -(Hmitad-htot+Rad)+Rad*sin(pi/4), 0.0)
    coord_circ2 = (-Rad*cos(pi/4), -(Hmitad-htot+Rad)+Rad*sin(pi/4), 0.0)

    arista_circ1  = mdb.models['Model-1'].rootAssembly.instances['Part-1'].edges.findAt((coord_circ1, ))[0:1]
    mdb.models['Model-1'].rootAssembly.seedEdgeBySize(
        edges=arista_circ1, 
        size=0.1, 
        deviationFactor=0.1, 
        constraint=FIXED
    )
    arista_circ2  = mdb.models['Model-1'].rootAssembly.instances['Part-1'].edges.findAt((coord_circ2, ))[0:1]
    mdb.models['Model-1'].rootAssembly.seedEdgeBySize(
        edges=arista_circ2, 
        size=0.1, 
        deviationFactor=0.1, 
        constraint=FIXED
    )

    coord_circ3 = (Rad, y_inicio-1.01*Rad, 0.0)
    coord_circ4 = (-Rad, y_inicio-1.01*Rad, 0.0)

    arista_circ3  = mdb.models['Model-1'].rootAssembly.instances['Part-1'].edges.findAt((coord_circ3, ))[0:1]
    mdb.models['Model-1'].rootAssembly.seedEdgeBySize(
        edges=arista_circ3, 
        size=0.2, 
        deviationFactor=0.1, 
        constraint=FIXED
    )
    arista_circ4  = mdb.models['Model-1'].rootAssembly.instances['Part-1'].edges.findAt((coord_circ4, ))[0:1]
    mdb.models['Model-1'].rootAssembly.seedEdgeBySize(
        edges=arista_circ4, 
        size=0.2, 
        deviationFactor=0.1, 
        constraint=FIXED
    )

    
    todas_las_caras = mdb.models['Model-1'].rootAssembly.instances['Part-1'].faces
    mdb.models['Model-1'].rootAssembly.setMeshControls(
        regions=todas_las_caras, 
        elemShape=QUAD,
        technique=FREE
    )

    tipo_plane_strain = ElemType(elemCode=CPE4, elemLibrary=STANDARD)

    mdb.models['Model-1'].rootAssembly.setElementType(
        regions=(todas_las_caras, ), 
        elemTypes=(tipo_plane_strain, )
    )

    # ==============================================================================
    # MESH GENERATION
    # ==============================================================================
    instancia_part = mdb.models['Model-1'].rootAssembly.instances['Part-1']

    mdb.models['Model-1'].rootAssembly.generateMesh(regions=(instancia_part, ))

    mdb.models['Model-1'].rootAssembly.regenerate()
    
    # ==============================================================================
    # JOB GENERATION
    # ==============================================================================
    indice_limpio = str(ind_i).strip().replace('.', '_')

    nombre_job = "steelD0_D1_l{}".format(indice_limpio)

    mdb.Job(
        name=nombre_job, 
        model='Model-1', 
        description='Simulation D1-F', 
        type=ANALYSIS, 
        atTime=None, 
        waitMinutes=0, 
        waitHours=0, 
        queue=None, 
        memory=90,              
        memoryUnits=PERCENTAGE, 
        getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, 
        nodalOutputPrecision=SINGLE, 
        echoPrint=OFF, 
        modelPrint=OFF, 
        historyPrint=OFF, 
        contactPrint=OFF, 
        userSubroutine='', 
        scratch='', 
        resultsFormat=ODB, 
        multiprocessingMode=DEFAULT, 
        numCpus=4,              
        numDomains=4,           
        numGPUs=0
    )

    # ==============================================================================
    # EXECUTION CONTROL
    # ==============================================================================
    mdb.saveAs(pathName=ruta)
    mdb.jobs[nombre_job].submit()
    mdb.jobs[nombre_job].waitForCompletion()

    
