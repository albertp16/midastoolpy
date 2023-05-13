# -*- coding: utf-8 -*-
"""
Created on Sat May 13 10:20:06 2023

@author: Albert Pamonag, M.Eng
"""
import math
from scipy.interpolate import interp1d

class windForce:
    def __init__(self,exposure,height,mri,gust_structure,gust_support_type,surface_area,wind_speed):
        self.exposure = exposure #Exposure 
        self.height = height
        self.mri = mri
        self.gust_structure = gust_structure 
        self.gust_support_type = gust_support_type
        self.surface_area = surface_area #project area
        self.wind_speed = wind_speed
    def airDensity(self):
        constant = 0.613 
        return constant
    def terrainExposureCoefficient(self):
        
        mult = 0.305 
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
        # print(tec)
        ##To select table
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

        if self.gust_structure == "structure" and self.gust_support_type == "wire-support":
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
            # print(table3d4a)
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
        ##Table 
        table3d9 = {
            "structural shape" : 1.6,
            "bus" : 1.0,
            "circular" : 0.90
        }
        return table3d9["bus"] 
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

test = windForce("B",11,mri,gust_structure,gust_support_type,sa_sa,91.111)
kzt = test.terrainExposureCoefficient()
ifw = test.importanceFactor()
grf = test.gustResponseFactor()
F = test.windForce()

'''
post insulator H : 2335mm x 315mm (circular)
surge arrester H: 3071mm x 250mm (rectangular)
'''



print('kzt = ' + str(kzt))
print('ifw = ' + str(ifw))
print('grf = ' + str(grf))
print('surface area (PI) = ' + str(sa_pi))
print('surface area (SA) = ' + str(sa_sa))
print('Wind Force (F) = ' + str(F/1000))
## apply to midas
print(3.35/4)

# ##return period 
# def returnPeriod(pa,n):
#     pn = 1 - math.pow(1-pa,n)
#     return pn
# rp = 1/2475
# print(rp)
# check = returnPeriod(rp,50)
# print(check)