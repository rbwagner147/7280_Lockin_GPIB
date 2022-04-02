# -*- coding: utf-8 -*-


import pyvisa
#import time as tm 
#import numpy as np 
#import matplotlib.pyplot as plt 


#%% Opens instrument 

rm = pyvisa.ResourceManager()
inst = rm.open_resource('GPIB0::12::INSTR')     # Open instrument, GPIB needs to be set manually
str_term = 'EOI'                                # Terminator string, 3 options on locking, needs to be set manually  

print(inst.query('ID ' + str_term))      


           


