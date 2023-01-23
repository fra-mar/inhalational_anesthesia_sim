#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 231204

Animated distrubution model. No controls
Gets pharma-physio data from script
"""
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from inh_pk_data import inh_drugs_data
#%%Physio and drug data in order: 
#blood(b/g),heart(t/b), kidney, liver, cns, muscle, fat, vrg

pk_data= inh_drugs_data()
drug= 'sevo'
drug_coefs= pk_data.loc[drug] #load bg and tb partition coefficients
vols= pk_data.loc['vols'] #load compartments volumnes
co_f= pk_data.loc['co_f'] #load fractional cardiac outputs per compartment

Veff= drug_coefs*vols #effective volumes

#%% Initial variables, partial pressures
Pdel= 8  #Vaporizer, initial pressure
Pcirc= 0
Palv= 0
Pheart= 0 
Pkidney= 0
Pliver= 0
Pcns=  0
Pmuscle= 0 
Pfat= 0 
Pvrg= 0
 

#%%Initial variables, other
t=0
duration= 10 #minutes
interval= 1  #s5

vol_circ= 6  #L
fgf= 6/60  #6L/min in seconds

V= 5/60 #6L/min MinuteVolume
Vd= V*0.15 #dead space
Va= V-Vd   #alveolar space
Vpulm= 0.5+1+1.5  #Vt + ExpReservV + ResVol
Valv= 4+0.5+1+1.5  #Alveolar volumne, same as Vpulm+InspReservVol

CO= 5/60 #L/sec
co_s= co_f * CO   #L/sec per organ

taus_min= Veff/(co_s*60) #time constants as per second
Pmv= 0   #partial pressure in mixed venous blood
Part= 0
rl_shunt= CO*0.1 #right to left shunt as a proportion of CO

sto= np.zeros((0,13)) #initialize storing array

#%%Start the plot
figure= plt.figure(figsize=(10,7))
ax= figure.add_subplot(111)
ax.set_ylim([0,8])
ax.set_xlim([0,duration*60])


l_circ, = ax.plot([],[],'y-',alpha= 0.5, label='Pcirc')
l_alv, = ax.plot([],[],'b-',alpha= 0.5, label='Palv')
l_art, = ax.plot([],[],'r-', label='Part')
l_cns, = ax.plot([],[],'g-',lw=3, label='Pcns')
l_musc, = ax.plot([],[], 'r-.', label= 'Pmusc')
l_fat, = ax.plot([],[],color= 'r',ls= ':', label='Pfat')


ax.set_xlabel( 'Time(min)')
ax.set_ylabel('drug(%)')
xticks= np.arange(0,duration*60,600)
ax.set_xticks(xticks)
ax.set_xticklabels(xticks/60)
ax.set_title(f'Uptake and distribution of {drug}. Millers model')
ax.grid()
ax.legend()

#%%Main loop

def gen(): #generates a number of frames if a condition is fullfilled
    frame = 0
    while True:
        frame += 1
        yield frame        
 
def animate(frame):
    

    global t, interval,sto, Pdel, Ppulm, Pcirc, Palv, Pmv, new_data
    global Part, Pheart, Pkidney, Pliver, Pcns, Pfat, Pvrg, Pmuscle
    
    Ppulm= (Palv*Va + Pcirc*Vd)/(Va+Vd)
    Pcirc= Pcirc + (fgf/vol_circ)*(Pdel-Pcirc) - V/Vpulm*(Pcirc-Ppulm)
    Palv= Palv + ((Va/Vpulm)*(Pcirc-Palv)) - (CO * drug_coefs[0]*(Palv-Pmv))/Valv
    
    Part= (Pmv*rl_shunt + Palv*(CO-rl_shunt))/CO
    Pheart= Pheart + (co_s[1]/(vols[1]*drug_coefs[1])) * (Part-Pheart)
    Pkidney= Pkidney + (co_s[2]/(vols[2]*drug_coefs[2])) * (Part-Pkidney)
    Pliver= Pliver + (co_s[3]/(vols[3]*drug_coefs[3])) * (Part-Pliver)   
    Pcns= Pcns + (co_s[4]/(vols[4]*drug_coefs[4])) * (Part-Pcns)
    Pmuscle= Pmuscle + (co_s[5]/(vols[5]*drug_coefs[5])) * (Part-Pmuscle)
    Pfat= Pfat + (co_s[6]/(vols[6]*drug_coefs[6])) * (Part-Pfat)
    Pvrg= Pvrg + (co_s[7]/(vols[7]*drug_coefs[7])) * (Part-Pvrg)
    
    array_Pi= np.array([Pheart, Pkidney, Pliver, Pcns, Pmuscle, Pfat, Pvrg])
    Pmv= sum( array_Pi*co_f[1:])

    new_data= np.array([t, Pdel, Pcirc, Palv, Part, Pmv])
    new_data= np.hstack((new_data,array_Pi))
    
    sto= np.vstack((sto, new_data))
    print(sto.shape)
    
    t= t+interval
    if t>60*60:
        Pdel= 1e-10 #almost zero
    
    l_circ.set_data(sto[:,0],sto[:,2])
    l_alv.set_data(sto[:,0],sto[:,3])
    l_art.set_data(sto[:,0],sto[:,4])
    l_cns.set_data(sto[:,0],sto[:,9])
    l_musc.set_data(sto[:,0],sto[:,10])
    l_fat.set_data(sto[:,0],sto[:,11])
    
    
    
    
    
    ax.collections.clear()
    
    return l_circ, l_cns,l_alv, l_art, l_musc, l_fat, 
    
#%% Animation function

ani= FuncAnimation(figure, func= animate,
                   repeat= False,
                   frames= gen,interval= 100,
                              blit=False)

plt.show()