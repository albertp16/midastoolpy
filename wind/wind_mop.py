# -*- coding: utf-8 -*-
"""
Created on Sat May 13 10:20:06 2023

@author: Albert Pamonag, M.Eng
"""
import math
from scipy.interpolate import interp1d

class windForce:
    
    """
    Calculate Wind Force per ASCE MOP 113

    Attributes
    ----------
    exposure : str
        exposure classification ['B'.'C'.'D']
    height : float
        ...
    mri : str
        ...
    gust_structure : str
        ...
    gust_support_type : str
        ...
    surface_area : float
        project wind surface area normal to the direction of wind (sq.m)
    wind_speed : float
        Basic wind speed, 3-s gust wind speed (m/s)
    """
    
    def __init__(self,exposure : str,height : float, mri : str, gust_structure : str ,gust_support_type : str ,surface_area : float ,wind_speed : float) -> float:
        self.exposure = exposure #Exposure 
        self.height = height
        self.mri = mri
        self.gust_structure = gust_structure 
        self.gust_support_type = gust_support_type
        self.surface_area = surface_area #project area
        self.wind_speed = wind_speed
        
    def airDensity(self):
        '''
        Air density factor, default value = 0.00256 (0.613 SI) 
        
        Returns:
        airDensity (float): Return constant value of air density 
        '''
        AIR_DENSITY = 0.613 
        return AIR_DENSITY
    def terrainExposureCoefficient(self):
        
        mult = 0.305 #factor convert the imperials into metric
        ht_metric = [] 
        
        tec = [
            [15,30,40,50,60,70,80,90,100], ## Height
            [0.57,0.70,0.76,0.81,0.85,0.89,0.93,0.96,0.99], ##for B
            [0.85,0.98,1.04,1.09,1.13,1.17,1.21,1,24,1.26], ##for C
            [1.03,1.16,1.22,1,27,1.31,1.34,1.38,1.40,1.43], ##for D
        ]
        
        for i in tec[0]:
            convert_ht = int(i)*mult
            ht_metric.append(convert_ht)

        tec.insert(1,ht_metric)
        if self.exposure == "B":
            tec_value = tec[2]
        elif self.exposure == "C":
            tec_value == tec[3]
        elif self.exposure == "D":
            tec_value = tec[4]
        
        limit_one = 15*mult
        limit_two = 100*mult

        if self.height <= limit_one:
            kz = tec_value[0]
        elif self.height >= limit_two:
            kz = tec_value[8]  
        else: 

            interpolating = interp1d(tec[1], tec_value)
            kz = interpolating(self.height)
        return  kz
    def basicWindSpeed(self):
        return self.wind_speed
    def importanceFactor(self):
        if self.mri == "50 years":
            ifw = 1.0
        elif self.mri == "100 years":
            ifw = 1.15
        return ifw
    def gustResponseFactor(self):

        if self.gust_structure == "structure" or self.gust_support_type == "wire-support":
            table3d4a = [ #Table 3-4a | Structure Response, Gsrf, for Wire-supporting
                [33,40,50,60,70,80,90,100], #height in imperial units
                [1.17,1.15,1.12,1.08,1.06,1.03,1.01,1.00], #for exposure B
                [0.96,0.95,0.94,0.92,0.91,0.89,0.88,0.88], #for exposure C
                [0.85,0.84,0.84,0.83,0.81,0.81,0.80] #for exposure D
            ]
            mult = 0.305 
            ht_metric = [] 
        
            for i in table3d4a[0]:
                convert_ht = int(i)*mult
                ht_metric.append(convert_ht)
    
            table3d4a.insert(1,ht_metric)
       
            if self.exposure == "B":
                table3d4a_value = table3d4a[2]
            elif self.exposure == "C":
                table3d4a_value == table3d4a[3]
            elif self.exposure == "D":
                table3d4a_value = table3d4a[4]        
            
            limit_one = table3d4a[1][0]
            limit_two = table3d4a[1][7]
            
            if self.height <= limit_one:
                grf = table3d4a_value[0]
            elif self.height >= limit_two:
                grf = table3d4a_value[7]  
            else: 
                interpolating = interp1d(table3d4a[1], table3d4a_value)
                grf = interpolating(self.height)        
        
        return grf 
    def forceCoefficient(self):

        table3d9 = {
            "structural shape" : 1.6,
            "bus" : 1.0,
            "circular" : 0.90
        }
        return table3d9["structural shape"] 
    def windSurfaceArea(self):
        return self.surface_area
    def windForce(self):
        q = self.airDensity() #constant
        kz = self.terrainExposureCoefficient() #unitless
        v = self.basicWindSpeed() #kph
        ifw = self.importanceFactor() #unitless
        grf = self.gustResponseFactor() #unitless
        cf = self.forceCoefficient() #unitless
        area = self.windSurfaceArea() #m2
        F = q*kz*math.pow(v,2)*ifw*grf*cf*area
        return F
    
sa_pi = 2.335*.315 
sa_sa = 3.071*.250   
mri = "50 years"
gust_structure = "structure" ##"wire and bus"
gust_support_type = "wire-support"
surface_area = 2.335*.315

test = windForce("B",11,mri,gust_structure,gust_support_type,sa_pi,91.111)
kzt = test.terrainExposureCoefficient()
ifw = test.importanceFactor()
grf = test.gustResponseFactor()
F = test.windForce()

'''
post insulator H : 2335mm x 315mm (circular)
surge arrester H: 3071mm x 250mm (rectangular)
'''

kz = 1.0
grf = 1.17 ##per Tabe 
cf = 1.6 
ifw = 1
kz = 1.15
v = 88.33

data = [
        ["SA",0.7902],
        ["CVT",1.6605],      
        ["CT",1.6605],
        ["CIT",1.7486], 
        ["DES",3.4948]
        ]
sa_area = 0.7902
cvt_area = 1.6605
ct_area = 1.6605
cit_area = 1.7486
des_area = 3.4948


sah = 3 + 0.2 + 3.4
cvth = 2.5 + 0.2 + 3.95
cth = 2.5 + 0.2 + 3.9
cith = 2.5 + 0.2 + 3.95
desh = 2.5 + 0.2 + 3

sah2 = 3 + 0.2
cvth2 = 2.5 + 0.2 
cth2 = 2.5 + 0.2 
cith2 = 2.5 + 0.2 
desh2 = 2.5 + 0.2 


saF = windForce("B",sah,mri,gust_structure,gust_support_type,sa_area,v)
cvtF = windForce("B",cvth,mri,gust_structure,gust_support_type,cvt_area,v)
ctF = windForce("B",cth,mri,gust_structure,gust_support_type,ct_area,v)
citF = windForce("B",cith,mri,gust_structure,gust_support_type,cit_area,v)
desF = windForce("B",desh,mri,gust_structure,gust_support_type,des_area,v)


# saF = windForce("B",11,mri,gust_structure,gust_support_type,sa_pi,v)
# print('kzt = ' + str(kzt))
# print('ifw = ' + str(ifw))
# print('grf = ' + str(grf))
# print('surface area (PI) = ' + str(sa_pi))
# print('surface area (SA) = ' + str(sa_sa))
# print('Wind Force (F) = ' + str(F/1000))
# ## apply to midas
print("SA " + str(saF.gustResponseFactor() ) + " kN")
print("CVT " + str(cvtF.gustResponseFactor() ) + " kN")
print("CT " + str(ctF.gustResponseFactor() ) + " kN")
print("CIT " + str(citF.gustResponseFactor() ) + " kN")
print("DEDS " + str(desF.gustResponseFactor() ) + " kN")


print("SA " + str(saF.windForce()/1000 ) + " kN")
print("CVT " + str(cvtF.windForce()/1000 ) + " kN")
print("CT " + str(ctF.windForce()/1000 ) + " kN")
print("CIT " + str(citF.windForce()/1000 ) + " kN")
print("DEDS " + str(desF.windForce()/1000 ) + " kN")


m_wind = desh*desF.windForce()/1000 
m_seis = desh2*5.75
print("DEDS wind " + str(m_wind/2 ) + " kN")
print("DEDS seis " + str(m_seis ) + " kN")

# SA wind 29.302578277783226 kN
# SA seis 3.04 kN

# CVT wind 62.182408421034076 kN
# CVT seis 15.957 kN

# CT wind 61.57546346527341 kN
# CT seis 10.368 kN

# CIT wind 65.48157745559782 kN
# CIT seis 15.525 kN

# ##return period 
# def returnPeriod(pa,n):
#     pn = 1 - math.pow(1-pa,n)
#     return pn
# rp = 1/2475
# print(rp)
# check = returnPeriod(rp,50)
# print(check)