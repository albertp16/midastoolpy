# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 20:45:16 2022

@author: albert pamonag (albertp16)
"""

import math

def toDegrees (angle):
    return angle * (math.pi / 180)

def period(constant,height):
    output = constant*math.pow(height,3/4)
    return output

def generateSampleData():
  string = '''
              ##Tool created by Albert Pamonag
              ##disclaimer: User is assumed to double check the values and input. creator is solely liable for the omitted error
              data = {
                  "structure" : "steel", #[steel,concrete,others]
                  "SPT" : "sd", ##Soil Profile Type [Sa,Sb,Sc,Sd,Se,Sf]
                  "ZF" : 0.4, ##Seismic zone factor [0.2,0.4]
                  "SST" : "A", ##Seismic source type [A,B,C]
                  "CD" : 6.6, ##closest distance to known seismic factor [float]
                  "IF" : 1, ##importance factor [float]
                  "R" : { ##Response Modification factor
                      "x" : 8,
                      "y" : 8
                  },
                  "hn" : { ##building height
                      "x" : 20,
                      "y" : 20
                  },
                  "angle" : {
                      "x" : 0,
                      "y" : 90
                  },
                  'case' : ["Ex","Ex +","Ex -","Ey","Ey +","Ey -"],
                  'eccentricity' : {
                      "x" : ["NONE","POS","NEG","NONE","NONE","NONE"],
                      "y" : ["NONE","NONE","NONE","NONE","POS","NEG"]
                  },
                  'acc' : ["NO","NO","NO","NO","NO","NO"],
                  'inherit' : ["NO","NO","NO","NO","NO","NO"]
              }'''
  return string

def staticSeismic(data):
    """
    Generate MGT format file

    Parameters
    ----------
    data : dict
        DESCRIPTION. To generate format file : generateSampleData()
    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    hnx = data['hn']['x'] #Building height at X
    hny = data['hn']['y'] #Building height at Y
    
    # Compute the period 
    if data["structure"] == "steel":
        CT_STEEL = 0.0853
        period_x = round(period(CT_STEEL,hnx),2)
        period_y = round(period(CT_STEEL,hny),2)
    elif data["structure"] == "concrete":
        CT_CONC = 0.0731
        period_x = round(period(CT_CONC,hnx),2)
        period_y = round(period(CT_CONC,hny),2)
    elif data["structure"] == "others":
        CT_OTHERS = 0.0488
        period_x = round(period(CT_OTHERS,hnx),2)
        period_y = round(period(CT_OTHERS,hny),2)
    
    ##Critical angle
    major_angle = data["angle"]["x"]
    minor_angle = data["angle"]["y"]
    
    radian_major = toDegrees(major_angle)
    radian_minor = toDegrees(minor_angle)
    
    major_scale_x = round(math.cos(radian_major),3)
    major_scale_y = round(math.sin(radian_major),3)
    
    minor_scale_x = round(math.cos(radian_minor),3)
    minor_scale_y = round(math.sin(radian_minor),3)

    static_case = data['case']
    
    scale_x = [major_scale_x,major_scale_x,major_scale_x,minor_scale_x,minor_scale_x,minor_scale_x]
    scale_y = [major_scale_y,major_scale_y,major_scale_y,minor_scale_y,minor_scale_y,minor_scale_y]
    
    ecc_x = data['eccentricity']['x']
    ecc_y = data['eccentricity']['y']
    
    acc_ecc = data['acc']
    inher_ecc = data['inherit']
    
    E_string = ''
    length = len(static_case)
    i = 0
    
    while i < length:
        E_title1 = '*USE-STLD, ' + static_case[i] + ''
        E_title2 = "*SEIS    ; Static Seismic Loads"
        E_line1 = "CODE=UBC1997, " + str(scale_x[i]) + " , " + str(scale_y[i]) + ", " + ecc_x[i] + ", "+ecc_y[i]+ ", " + acc_ecc[0] + ", " + inher_ecc[0] + ", , 0" ## SCALE X, SCALE Y, ECCEX[POS,NEG,NONE], EECEY[POS,NES,NONE], TORACC[YES,NP], INHERENT[YES,NO]
        E_line2 = "        " + str(data["SPT"]) + ", " + str(data["ZF"]) + ", "+str(data["SST"])+", " + str(data["CD"]) + ", " + str(data["IF"]) + ", " + str(period_x) + ", " + str(period_y) + ", " + str(data["R"]["x"]) + ", " + str(data["R"]["y"]) + ", 0, 0"
        E_finish = '; End of data for load case [' + static_case[i] +'] -------------------------";'
    
        E_string += E_title1 + " \r\n " + E_title2 + " \r\n " + E_line1 + " \r\n " + E_line2 + " \r\n " + E_finish + "\r\n";
        i = i + 1
    return E_string

def plotRS(data):
    return 0