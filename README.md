# AbaFracCC: Python implementation of the Coupled Criterion in Abaqus (Finite Fracture Mechanics) 
**Sara Jiménez-Alfaro**$^{1,*}$, **Luis Miguel Ferreira**$^{1,2}$, **Zaarena Gani**$^3$, **Vladislav Mantič**$^1$, and **Luis Távara**$^1$

$^1$ *Departamento de Mecánica de Medios Continuos y Teoría de Estructuras. Escuela Técnica Superior de Ingeniería, Universidad de Sevilla, Camino de los descubrimientos, s/n, 41092, Seville, Spain.*  
$^2$ *Departamento de Mecánica de Medios Continuos y Teoría de Estructuras. Escuela Politécnica Superior, Universidad de Sevilla, Virgen de África, 7, 41011, Seville, Spain.*  
$^3$ *Department of Mechanical Engineering, University College London, Torrington Place, WC1E 7JE, London, United Kingdom*  

$^*$ *Contact:* [sjimenezalfaro@us.es]

The code is structured into two main sequential modules:

**Finite Element Method Module** 


**Coupled Criterion Post-processing Module** 

This code solves the minimization problem associated with the Coupled Criterion. It requires two inputs:

* **Elastic strain energy files:** Four `.dat` files located in the `energy_output` directory, containing the evolution of the elastic strain energy along the expected crack path obtained from the previous module for a representative displacement of $U=1$. Each file represents one of the four geometric configurations studied for the $0^\circ$-oriented printed steel.
* **Tensile stress files:** Four `.dat` files located in the `stress_output` directory, containing the evolution of the tensile stress along the expected crack path obtained from the previous module for a representative displacement of $U=1$. Each file represents one of the four geometric configurations studied for the $0^\circ$-oriented printed steel.
