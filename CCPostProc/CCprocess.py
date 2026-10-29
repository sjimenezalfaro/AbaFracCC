# APPLICATION OF THE COUPLED CRITERION TO ESTIMATE THE CRITICAL LOAD
import numpy as np
from math import *
from scipy.interpolate import interp1d

def CCprocess(CC_stress, CC_energy, Scv, Gcv):
        # Yp - position, Sp - Tensile stress, W - elastic strain energy, W0 - elastic strain energy in the uncracked configuration
        Yp, Sp, W = CC_stress[0,:], CC_stress[1,:], CC_energy
        W0 = W[0]
        # Incremental energy release rate
        Ginc = np.divide((W0*np.ones(len(W)-1) - W[1:len(W)]),10*Yp[1:len(W)])
        Yp, Sp = Yp[1:], Sp[1:]
        # Only positive values of the tensile stress will lead to crack nucleation
        mask = Sp >= 0     
        Yp, Sp, Ginc = Yp[mask], Sp[mask], Ginc[mask]
        # Initial matrix of critical load
        UCrit = np.zeros((len(Scv), len(Gcv)))
        FCrit = np.zeros((len(Scv), len(Gcv)))
        # Calculation of the critical load
        for i, Sc in enumerate(Scv):
                Sp_norm = np.divide(Sp,Sc)
                Us = np.divide(1,Sp_norm)
                for j, Gc in enumerate(Gcv):
                        Ginc_norm = np.divide(Ginc,Gc)
                        Ug = np.sqrt(np.divide(1,Ginc_norm))
                        U = np.maximum(Ug,Us)
                        UCritIndex = np.argmin(U)
                        # Interpolation 
                        if UCritIndex > 0 and UCritIndex < len(U)-1:
                                indices = [UCritIndex - 1, UCritIndex, UCritIndex + 1]
                        elif UCritIndex == 0:
                                indices = [UCritIndex, UCritIndex + 1, UCritIndex + 2]
                        else:
                                indices = [UCritIndex - 2, UCritIndex - 1, UCritIndex]
                        Yp_Interp = Yp[indices]
                        Ug_Interp = Ug[indices]
                        Us_Interp = Us[indices]
                        interpUgFunc = interp1d(Yp_Interp, Ug_Interp, kind='quadratic')
                        interpUsFunc = interp1d(Yp_Interp, Us_Interp, kind='quadratic')
                        Yp_Fine = np.linspace(Yp_Interp[0], Yp_Interp[-1], 1000)
                        Ug_Fine = interpUgFunc(Yp_Fine)
                        Us_Fine = interpUsFunc(Yp_Fine)
                        
                        U_Fine = np.maximum(Ug_Fine, Us_Fine)
                        UCritIndexFine = np.argmin(U_Fine)

                        UCrit [i,j] = U_Fine[UCritIndexFine]
                        FCrit [i,j] = 2*UCrit[i,j]*W0
                        # Calculation of the nucleation length length
                        # YpCrit = Yp_Fine[UCritIndexFine]

        return UCrit,FCrit

