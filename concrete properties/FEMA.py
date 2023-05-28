# -*- coding: utf-8 -*-
"""
Created on Fri May 19 13:58:59 2023

@author: albert pamonag
"""
import math
import matplotlib.pyplot as plt

##Acceptance Cateria
IO = 2 
LS = 4
CP = 6 

MY = 1
DY = 0
alpha = 0.05

##A,B,C,D,E
ma,mb,mc,md,me = 0,1,6,6.3,8
da,db,dc,dd,de = 0,1,1.25,0.2,0.2

mmy = [-me,-md,-mc,-mb,ma,mb,mc,md,me] 
ddy = [-de,-dd,-dc,-db,da,db,dc,dd,de]

fig, ax = plt.subplots(figsize=(15,15))
ax.plot(mmy, ddy,color="red")

ax.set(xlabel="M/My", ylabel="D/Dy",
            title= "Properties Inelastic hinge")
ax.grid()
plt.legend()
plt.show()
