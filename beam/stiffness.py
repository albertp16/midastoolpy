# -*- coding: utf-8 -*-
"""
BEAM STIFFNESS CALCULATOR

Created on Sun May 28 16:31:52 2023

@author: albert pamonag
"""

def typeTwo(rho,beam_w,d_eff,internia_g):
    '''
    NSCP 2015 Section 406.6.3 | Section Properties 
    
    Parameters
    ----------
    rho : TYPE
        DESCRIPTION. Steel Ratio of the cross-section
    beam_w : TYPE
        DESCRIPTION. beam width
    d_eff : TYPE
        DESCRIPTION.
    internia_g : TYPE
        DESCRIPTION. Internia

    Returns
    -------
    result : TYPE
        DESCRIPTION.

    '''
    result = (0.10 + 0.25*rho)*(1.2 - 0.2*(beam_w/d_eff))*internia_g
    minimum = 0.25*internia_g
    maximum = 0.5*internia_g
    if(minimum > result):
        return minimum
    elif(maximum < result):
        return maximum
    else:
        result


