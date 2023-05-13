# -*- coding: utf-8 -*-
"""
Created on Sat May 13 19:58:24 2023

@author: albert pamonag
"""

import math


phi_tension = 0.75 
phi_shear = 0.65
phi_pullout = 0.70

def steelTensionCheck(phi,ase,futa):
    output = phi*ase*futa
    return output

def steelShearCheck(phi,ase,futa):
    output = phi*0.60*ase*futa
    return output

def pullOutCheck(phi,psi_p,np):
    np = 8*abrg*fc
    output = phi*psi_p*np
    return output
