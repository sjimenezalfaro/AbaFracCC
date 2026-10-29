import time
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import cm
from matplotlib.colors import PowerNorm
from scipy.interpolate import RegularGridInterpolator, griddata
from CCprocess import CCprocess

# =====================================================================
# LATEX FONT
# =====================================================================
x = 20
plt.rcParams.update({
    "text.usetex": True,            
    "font.family": "serif",         
    "font.serif": ["Computer Modern Roman", "Times New Roman", "DejaVu Serif"],
    "font.size": x,                 
    "axes.labelsize": x,           
    "axes.titlesize": x,
    "xtick.labelsize": x,          
    "ytick.labelsize": x,
    "legend.fontsize": x,
    "axes.linewidth": 0.8,          
    "grid.linewidth": 0.5,          
    "grid.alpha": 0.5               
})

# =====================================================================
# RESULTS
# =====================================================================
CC_stress_SteelD0_S1 = np.loadtxt("./stress_output/stress_SteelD0_S1.dat", unpack=True)
CC_energy_SteelD0_S1 = np.loadtxt("./energy_output/energy_SteelD0_S1.dat", unpack=True)
CC_stress_SteelD0_S2 = np.loadtxt("./stress_output/stress_SteelD0_S2.dat", unpack=True)
CC_energy_SteelD0_S2 = np.loadtxt("./energy_output/energy_SteelD0_S2.dat", unpack=True)
CC_stress_SteelD0_D1 = np.loadtxt("./stress_output/stress_SteelD0_D1.dat", unpack=True)
CC_energy_SteelD0_D1 = np.loadtxt("./energy_output/energy_SteelD0_D1.dat", unpack=True)
CC_stress_SteelD0_D2 = np.loadtxt("./stress_output/stress_SteelD0_D2.dat", unpack=True)
CC_energy_SteelD0_D2 = np.loadtxt("./energy_output/energy_SteelD0_D2.dat", unpack=True)

# =====================================================================
# COUPLED CRITERION ANALYSIS
# =====================================================================
# Material properties (MPa, )
E, nu = 168.e3, 0.3
# Fracture properties
Scv = np.linspace(start=500, stop=2500, num=100)
Gcv = np.linspace(start=40, stop=90, num=100)                  
Kcv = np.sqrt(Gcv * E / (1 - nu**2)) / sqrt(1000)
Kc_mesh, Sc_mesh = np.meshgrid(Kcv, Scv)

# Critical displacement, force, for each configuration
UCrit_SteelD0_S1, FCrit_SteelD0_S1 = CCprocess(CC_stress_SteelD0_S1, CC_energy_SteelD0_S1, Scv, Gcv)
UCrit_SteelD0_S2, FCrit_SteelD0_S2 = CCprocess(CC_stress_SteelD0_S2, CC_energy_SteelD0_S2, Scv, Gcv)
UCrit_SteelD0_D1, FCrit_SteelD0_D1 = CCprocess(CC_stress_SteelD0_D1, CC_energy_SteelD0_D1, Scv, Gcv)           
UCrit_SteelD0_D2, FCrit_SteelD0_D2 = CCprocess(CC_stress_SteelD0_D2, CC_energy_SteelD0_D2, Scv, Gcv) 

# Experimental critical force (Newton)
FCritExp_SteelD0_D1 = 17501
FCritExp_SteelD0_D2 = 16039
FCritExp_SteelD0_S1 = 47883
FCritExp_SteelD0_S2 = 40967

# =====================================================================
# ERROR CALCULATION BETWEEN EXPERIMENTAL AND NUMERICAL CRITICAL FORCES
# =====================================================================

# Difference
diff_SteelD0_D1 = FCrit_SteelD0_D1 - FCritExp_SteelD0_D1
diff_SteelD0_D2 = FCrit_SteelD0_D2 - FCritExp_SteelD0_D2
diff_SteelD0_S1 = FCrit_SteelD0_S1 - FCritExp_SteelD0_S1
diff_SteelD0_S2 = FCrit_SteelD0_S2 - FCritExp_SteelD0_S2

# Cuadratic error 
diff_sq_D1 = (FCrit_SteelD0_D1 - FCritExp_SteelD0_D1)**2 / FCritExp_SteelD0_D1**2
diff_sq_D2 = (FCrit_SteelD0_D2 - FCritExp_SteelD0_D2)**2 / FCritExp_SteelD0_D2**2
diff_sq_S1 = (FCrit_SteelD0_S1 - FCritExp_SteelD0_S1)**2 / FCritExp_SteelD0_S1**2
diff_sq_S2 = (FCrit_SteelD0_S2 - FCritExp_SteelD0_S2)**2 / FCritExp_SteelD0_S2**2  

diff = diff_sq_D1 + diff_sq_D2 + diff_sq_S1 + diff_sq_S2
# Root Mean Square Error (%)
rms = 100 * np.sqrt(0.25 * diff)  

# =====================================================================
# DETERMINATION OF THE MINIMUM ERROR
# =====================================================================
# Obtiene los índices (fila, columna) del valor mínimo en la matriz 'diff'
min_idx = np.unravel_index(np.argmin(diff), diff.shape)
# Fracture properties (Kc [MPa \sqrt{m}], Gc[J/m^2], Sc[MPa] )
best_Sc = Scv[min_idx[0]]  
best_Gc = Gcv[min_idx[1]]  
best_Kc = Kc_mesh[min_idx]  
min_diff = rms[min_idx]

print(f"--- OPTIMAL FRACTURE PROPERTIES ---")
print(f"Tensile strength : {best_Sc:.2f} MPa")
print(f"Critical Energy Release Rate: {best_Gc:.2f} J/m²")
print(f"Fracture Toughness : {best_Kc:.2f} MPa*m^(1/2)")
print(f"Minimum Root Mean Square Error : {min_diff:.6e} %")

# =====================================================================
# FIGURE 1: REPRESENTATION OF THE RMS AREA AND THE PROJECTION 
# =====================================================================
plt.figure(figsize=(9, 7))
plt.tick_params(axis="both")

# Region where RMS < 5%
plt.contourf(
    Kc_mesh, Sc_mesh, rms, 
    levels=[0, 5], 
    colors=['#a1dab4'], 
    alpha=0.4, 
    zorder=5
)

corte_rms = plt.contour(
    Kc_mesh, Sc_mesh, rms, 
    levels=[5], 
    colors=['#238b45'], 
    linestyles='--', 
    linewidths=1.5, 
    zorder=6
)


plt.clabel(corte_rms, inline=False, fmt=lambda x: r"$\mathrm{RMS} < 5\%$", fontsize=12)
corte_SteelD0_D1 = plt.contour(Kc_mesh, Sc_mesh, diff_SteelD0_D1, levels=[0], colors='red', linewidths=2, zorder=3)
plt.clabel(corte_SteelD0_D1, inline=1, fmt="$\mathrm{D1-F}$")
corte_SteelD0_D2 = plt.contour(Kc_mesh, Sc_mesh, diff_SteelD0_D2, levels=[0], colors='red', linewidths=2, zorder=3)
posicion_p2 = [(95, 1340)] 
plt.clabel(corte_SteelD0_D2, manual=posicion_p2, inline=True, fmt="$\mathrm{D2-F}$")
corte_SteelD0_S1 = plt.contour(Kc_mesh, Sc_mesh, diff_SteelD0_S1, levels=[0], colors='blue', linewidths=2, zorder=3)
posicion_p3 = [(95.15, 1240)] 
plt.clabel(corte_SteelD0_S1, manual=posicion_p3, inline=True, fmt="$\mathrm{S1-F}$")
corte_SteelD0_S2 = plt.contour(Kc_mesh, Sc_mesh, diff_SteelD0_S2, levels=[0], colors='blue', linewidths=2, zorder=3)
posicion_p4 = [(93.09, 1340)] 
plt.clabel(corte_SteelD0_S2, manual=posicion_p4, inline=True, fmt="$\mathrm{S2-F}$")

# Calculation of the area between projections
kc_fino = np.linspace(Kcv.min(), Kcv.max(), 1000)
sc_fino = np.linspace(Scv.min(), Scv.max(), 1000)
Kc_mesh_fino, Sc_mesh_fino = np.meshgrid(kc_fino, sc_fino)

def refine_matrix(x_orig, y_orig, z_orig):
    interp = RegularGridInterpolator((y_orig, x_orig), z_orig, bounds_error=False, fill_value=None)
    puntos = np.array([Sc_mesh_fino.ravel(), Kc_mesh_fino.ravel()]).T
    return interp(puntos).reshape(Sc_mesh_fino.shape)

diff_p1_fina = refine_matrix(Kcv, Scv, diff_SteelD0_D1)
diff_p2_fina = refine_matrix(Kcv, Scv, diff_SteelD0_D2)
diff_p3_fina = refine_matrix(Kcv, Scv, diff_SteelD0_S1)
diff_p4_fina = refine_matrix(Kcv, Scv, diff_SteelD0_S2)

red_condition = (diff_p1_fina < 0) & (diff_p2_fina > 0)
blue_condition = (diff_p3_fina < 0) & (diff_p4_fina > 0)
mask_solape = red_condition & blue_condition

plt.contourf(Kc_mesh_fino, Sc_mesh_fino, mask_solape.astype(int), levels=[0.5, 1.5], colors=['#fff176'], alpha=0.7, zorder=2)

plt.scatter(best_Kc, best_Sc, color='green', s=80, zorder=2)
patch_rms = mpatches.Patch(color='#a1dab4', alpha=0.5, label=r"$\mathrm{RMS} < 5\%$")
patch_solape = mpatches.Patch(color='#fff176', alpha=0.7, label=r"$\mathrm{Overlap\ area}$")
plt.legend(handles=[patch_rms, patch_solape], loc='upper left')

plt.xlabel(r"$K_c$ [$\mathrm{MPa} \sqrt{\mathrm{m}}$]")
plt.ylabel(r"$\sigma_c$ [$\mathrm{MPa}$]")
plt.grid(True, linestyle='--', alpha=0.5)
plt.xlim(90, 115)

plt.tight_layout()
plt.savefig('./output/projection_steel0.svg', format='svg', bbox_inches='tight', dpi=300)

# =====================================================================
# FIGURA 2: REPRESENTATION OF THE TOTAL ERROR (3D)
# =====================================================================
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")

surf = ax.plot_surface(
    Kc_mesh, Sc_mesh, diff,
    cmap=cm.viridis,
    edgecolor="none",
    alpha=0.9,
    antialiased=True
)

ax.set_xlabel(r"$K_c$ [$\mathrm{MPa} \sqrt{\mathrm{m}}$]", labelpad=10)
ax.set_ylabel(r"$S_c \quad [\mathrm{MPa}]$", labelpad=10)
ax.set_zlabel(r"$\mathrm{Error} \quad [-]$", labelpad=10)

cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, pad=0.1)
cbar.set_label(r"$\sum (\Delta F_{\mathrm{crit}})^2 / F_{\mathrm{exp}}^2$")
ax.view_init(elev=25, azim=135)

plt.tight_layout()
plt.savefig("./output/diff_steel0_3D.svg", format="svg", bbox_inches="tight", dpi=300)

# =====================================================================
# FIGURE 3: HEATMAP WITH RMS (%)
# =====================================================================
from matplotlib.colors import BoundaryNorm

max_rms = np.ceil(rms.max() / 5.0) * 5.0
niveles = np.arange(0, max_rms + 5, 5)  
cmap = plt.get_cmap('viridis', len(niveles) - 1)
norm = BoundaryNorm(niveles, ncolors=cmap.N)

fig, ax = plt.subplots(figsize=(10, 8))
surf = ax.contourf(
    Kc_mesh,
    Sc_mesh,
    rms,
    levels=niveles,
    cmap=cmap,
    norm=norm,
    extend='max'  
)
ax.contour(
    Kc_mesh,
    Sc_mesh,
    rms,
    levels=niveles,
    colors='black',
    linewidths=0.4,
    alpha=0.4
)

plt.scatter(best_Kc, best_Sc, color='limegreen', edgecolor='black', s=90, zorder=5)
ax.set_xlabel(r"$K_c$ [$\mathrm{MPa} \sqrt{\mathrm{m}}$]", labelpad=10)
ax.set_ylabel(r"$\sigma_c \quad [\mathrm{MPa}]$", labelpad=10)
cbar = fig.colorbar(surf, ax=ax, ticks=niveles, shrink=0.8, aspect=20, pad=0.1)
cbar.set_label(r"$\mathrm{RMS} \quad [\%]$")

plt.tight_layout()
plt.savefig('./output/rms_steel0_heatmap.svg', format='svg', bbox_inches='tight', dpi=300)

# =====================================================================
# FIGURE 5: 3D SURFACE FORCE (D0_D1) AND INTERSECTION 
# =====================================================================
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection="3d")
ax.tick_params(axis="both")

COLOR_GRIS_CLARO = "#d9d9d9"
COLOR_GRIS_OSCURO = "#505050"
COLOR_LINEA_CORTE = "#ff007f"

FCritExp_SteelD0_D1_kN = FCritExp_SteelD0_D1 / 1000.0
FCrit_SteelD0_D1_kN = FCrit_SteelD0_D1 / 1000.0

mask_superior = FCrit_SteelD0_D1_kN >= FCritExp_SteelD0_D1_kN

FCrit_SteelD0_D1_top = np.where(mask_superior, FCrit_SteelD0_D1_kN, np.nan)
FCrit_SteelD0_D1_bottom = np.where(~mask_superior, FCrit_SteelD0_D1_kN, np.nan)
FCrit_exp_top = np.where(~mask_superior, FCritExp_SteelD0_D1_kN, np.nan)
FCrit_exp_bottom = np.where(mask_superior, FCritExp_SteelD0_D1_kN, np.nan)

# Graficamos capas inferiores y superiores
ax.plot_surface(Kc_mesh, Sc_mesh, FCrit_exp_bottom, color=COLOR_GRIS_CLARO, alpha=1.0, rstride=1, cstride=1, antialiased=True, zorder=1)
ax.plot_surface(Kc_mesh, Sc_mesh, FCrit_SteelD0_D1_bottom, color=COLOR_GRIS_OSCURO, alpha=1.0, rstride=1, cstride=1, antialiased=True, zorder=2)
ax.plot_surface(Kc_mesh, Sc_mesh, FCrit_exp_top, color=COLOR_GRIS_CLARO, alpha=1.0, rstride=1, cstride=1, antialiased=True, zorder=3)
ax.plot_surface(Kc_mesh, Sc_mesh, FCrit_SteelD0_D1_top, color=COLOR_GRIS_OSCURO, alpha=1.0, rstride=1, cstride=1, antialiased=True, zorder=4)

# Línea de intersección 3D
diff_matriz = FCrit_SteelD0_D1_kN - FCritExp_SteelD0_D1_kN

contour_fig = plt.figure()
ax_aux = contour_fig.add_subplot(111)
cs = ax_aux.contour(Kc_mesh, Sc_mesh, diff_matriz, levels=[0])
plt.close(contour_fig)

paths = cs.get_paths() if hasattr(cs, "get_paths") else cs.collections[0].get_paths()

for path in paths:
    v = path.vertices
    x_corte = v[:, 0]
    y_corte = v[:, 1]

    puntos_malla = np.column_stack((Kc_mesh.ravel(), Sc_mesh.ravel()))
    valores_z = FCrit_SteelD0_D1_kN.ravel()
    z_corte = griddata(puntos_malla, valores_z, (x_corte, y_corte), method="linear")

    ax.plot(x_corte, y_corte, z_corte, color=COLOR_LINEA_CORTE, linewidth=4.5, zorder=100)

ax.set_xlabel(r"$K_{\mathrm{c}}$ [$\mathrm{MPa} \sqrt{\mathrm{m}}$]", labelpad=18)
ax.set_ylabel(r"$\sigma_{\mathrm{c}}$ [$\mathrm{MPa}$]", labelpad=18)
ax.set_zlabel(r"$F_{\mathrm{crit}}$ [$\mathrm{kN}$]", labelpad=12)

patch0 = mpatches.Patch(color=COLOR_GRIS_OSCURO, label=r"$\mathrm{Numerical}$")
patch1 = mpatches.Patch(color=COLOR_GRIS_CLARO, label=r"$\mathrm{Experimental}$")
line_patch = plt.Line2D([0], [0], color=COLOR_LINEA_CORTE, lw=3, label=r"$\mathrm{Intersection}$")

ax.legend(handles=[patch0, patch1, line_patch], fontsize=14, loc="center right", bbox_to_anchor=(-0.05, 0.5))
ax.view_init(elev=25, azim=-55)

plt.tight_layout()
plt.savefig("./output/surface_steelS1_F.pdf", format="pdf", bbox_inches="tight", dpi=400)
