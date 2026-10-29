# AbaFracCC: Numerical estimation of the fracture toughness via Coupled Criterion in Abaqus
**Sara Jiménez-Alfaro**$^{1,*}$, **Luis Miguel Ferreira**$^{1,2}$, **Zaarena Gani**$^3$, **Vladislav Mantič**$^1$, and **Luis Távara**$^1$

$^1$ *Departamento de Mecánica de Medios Continuos y Teoría de Estructuras. Escuela Técnica Superior de Ingeniería, Universidad de Sevilla, Camino de los descubrimientos, s/n, 41092, Seville, Spain.*  
$^2$ *Departamento de Mecánica de Medios Continuos y Teoría de Estructuras. Escuela Politécnica Superior, Universidad de Sevilla, Virgen de África, 7, 41011, Seville, Spain.*  
$^3$ *Department of Mechanical Engineering, University College London, Torrington Place, WC1E 7JE, London, United Kingdom*  

$^*$ *Contact:* [sjimenezalfaro@us.es]

The code is structured into two main sequential modules:

**Finite Element Method Module** 


**Coupled Criterion Post-processing Module** 

This code is located in CCPostProc, and it solves the minimization problem associated with the Coupled Criterion. It requires two inputs:

* **Elastic strain energy files:** Four `.dat` files located in the `energy_output` directory, containing the evolution of the elastic strain energy along the expected crack path obtained from the previous module for a representative displacement of $U=1$. Each file represents one of the four geometric configurations studied for the $0^\circ$-oriented printed steel.
* **Tensile stress files:** Four `.dat` files located in the `stress_output` directory, que contienen una matriz de dos columnas. La segunda columna se corresponde con la evolution of the tensile stress along the expected crack path obtained from the previous module for a representative displacement of $U=1$. La primera columna se corresponde con la posición a lo largo del expected crack path donde dicha tensión es evaluada. Each file represents one of the four geometric configurations studied for the $0^\circ$-oriented printed steel.

The main code in this module is CCPostProc.py. This code has the following structure:

Imagen con la estructura del codigo

The execution of the Coupled Criterion is carried out in the `CCprocess.py` script. This module outputs two primary matrices: Ucrit and Fcrit:

* **Ucrit:** Contains the critical applied displacements required for crack nucleation across a wide range of fracture properties, namely the tensile strength ($\sigma_c$) and the critical energy release rate ($G_c$). In this matrix, each row corresponds to a specific $\sigma_c$ value, while each column corresponds to a $G_c$ value.
* **Fcrit:** Stores the corresponding critical forces, calculated from the critical displacements using the stiffness of the structure.
 
