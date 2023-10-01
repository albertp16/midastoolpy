# -*- coding: utf-8 -*-
"""
Created on Sun May 28 16:46:44 2023

@author: alber
"""

'''
*FLOADTYPE    ; Define Floor Load Type
; NAME, DESC                                           ; 1st line
; LCNAME1, FLOAD1, bSBU1, ..., LCNAME8, FLOAD8, bSBU8  ; 2nd line
   Laboratory, 
   LL, -2.88, YES, SDL, -2.64, NO, DL, -2.95, NO
   Common Area, 
   LL, -3.8, YES, SDL, -2.64, NO, DL, -2.95, NO
   T&B, 
   LL, -2.88, YES, SDL, -2.64, NO, DL, -2.95, NO
   Utility Room, 
   LL, -7.2, YES, SDL, -3.84, NO, DL, -2.95, NO
   Elevator Lobby, 
   LL, -4.8, YES, SDL, -1.44, NO, DL, -2.95, NO
   Canopy, 
   LL, -1, YES, SDL, -1, NO, DL, -2.95, NO
'''

conc_uw = 23.6 #concrete unit weight
tslab = 0.125 #slab thickness
Z_FACTOR = -1 #gravity load 

data = [
        ["laboratory"],
        ["Common Area"],
        ["T&B"],
        ["Utility Room"],
        ["Elevator Lobby"],
        ["Canopy"]
        ]

print(data)

# def addDetail(dict_input):
#     output : {
#         "name" : 
#         "static" : 
#         "a"
        
#         }