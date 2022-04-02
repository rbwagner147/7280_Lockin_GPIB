# -*- coding: utf-8 -*-


import pyvisa
import time as tm 
#import numpy as np 
import matplotlib.pyplot as plt 


#%% Opens instrument 

rm = pyvisa.ResourceManager()
inst = rm.open_resource('GPIB0::12::INSTR')     # Open instrument, GPIB address needs to be set manually
str_term = 'EOI'                                # Terminator string, 3 options in lock-in comms menu, correct str needs to be set manually  

#%% Test queries  

print('ID = ', inst.query('ID ' + str_term))        # Returns instrument identification 
print('MAG = ', inst.query('MAG. ' + str_term))     # Returns signal magnitude singal
print('PHA = ',inst.query('PHA. ' + str_term))      # Returns signal magnitude phase
print('OA = ',inst.query('OA. ' + str_term))        # Returns the ossliator amplitude in volts 
print('Curve Status = ',inst.query('M ' + str_term))        # Returns the status of the curve aquisition system
print(' Status Byte = ',(inst.query('ST ' + str_term)).format(42))        # Returns the status of the curve aquisition system

print('FSTART = ', inst.query('FSTART. ' + str_term))        # Returns instrument identification 
print('FSTOP = ', inst.query('FSTOP. ' + str_term))     # Returns signal magnitude singal
print('FSTEP = ',inst.query('FSTEP. ' + str_term))      # Returns signal magnitude phase



#%% Data aquistion: Adapted from page 6-34 in instrument manual 

Npts = 91

inst.write('OA. 0.3E0 ' + str_term)     # Sets the ossliator amplitude in V
inst.write('OF. 100.0 ' + str_term)     # Sets the ossliator frequency in Hz

inst.write('SEN 27 ' + str_term)

# Set up frequency sweep 

inst.write('FSTART. 100 ' + str_term)  
inst.write('FSTOP.  1000 ' + str_term)
inst.write('FSTEP. 10 1 ' + str_term)
inst.write('SRATE. 0.05 ' + str_term)


inst.write('NC ' + str_term)           # Clear and reset curve buffer
inst.write('CBD 32796 ' + str_term)       #Stores Magnitude, Phase, Sensitivity and Frequency
#inst.write('CBD ' + str(0b10011) + str_term)       # Stores X channel output, Y channel output and sensitivity (i.e. bits 0, 1 and 4)
inst.write('LEN 91 ' + str_term)     # Number of points = 100 Hz × 10 seconds
inst.write('STR 50 ' + str_term)       # Store a point every 10 ms (1/100 Hz)
inst.write('SWEEP 9 '+ str_term)

inst.write('TD ' + str_term)     # Acquires data
while int(inst.query('M ' + str_term).split(',')[0]) ==  1: 
    print('Curve Status = ',inst.query('M ' + str_term))        #As the acquisition is running, the M command reports the status of the curve
    tm.sleep(1)


# Transfers data

Mag = []
Pha = []
Sens = []
Freq = []


print(inst.write('DC. 2 ' + str_term))     
for i in range(0,Npts): 
    print('stb = ', bin(inst.stb)[9])
    Mag.append(float(inst.read()))

print(inst.write('DC. 3 ' + str_term))     
for i in range(0,Npts): 
    print('stb = ', bin(inst.stb)[9])
    Pha.append(float(inst.read()))
    
print(inst.write('DC. 15 ' + str_term))    
for i in range(0,Npts): 
    print('stb = ', bin(inst.stb)[9])
    Freq.append(float(inst.read()))



#%% Plot data 

plt.figure() 
plt.subplot(2,1,1); plt.ylabel('Amplitude'); plt.plot(Freq,Mag,'.')
plt.subplot(2,1,2); plt.ylabel('Phase'); plt.plot(Freq,Pha,'.')

