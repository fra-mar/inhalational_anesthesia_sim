#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 17:44:33 2022

%Easy model to test equilibration of anesthetic circuit with
%vaporizer
%The integration equation is added to check for differences in 
%performace of the "differences" equation
"""
from matplotlib import pyplot as plt
import numpy as np
from inh_pk_data import inh_drugs_data
#%%Physiopharma data in order: 
#blood(b/g),heart(t/b), kidney, liver, cns, muscle, fat, vrg

pk_data= inh_drugs_data()
drug= 'sevo'
drug_coefs= pk_data.loc[drug]
vols= pk_data.loc['vols']
co_f= pk_data.loc['co_f']

#%% Initial variables, partial pressures
Pdel= 8; #Vaporizer, initial pressure
Pcirc= 0
Pheart= 0
Pkidney= 0
Pliver= 0
Pcns= 0
Pmuscle= 0
Pfat= 0
Pvrg= 0

Palv= 0

#%%Initial variables, other
t=0;
duration= 90 #minutes
interval= 1  #s

vol_circ= 6  #L
fgf= 6/60  #6L/min in seconds

V= 5/60; #6L/min MinuteVolume
Vd= V*0.15
Va= V-Vd
Vpulm= 0.5+1+1.5  #Vt + ExpReservV + ResVol
Valv= 4+0.5+1+1.5  #Alveolar volumne, same as Vpulm+InspReservVol

CO= 5/60 #L/sec
co_s= co_f * CO   #L/sec per organ
Veff= drug_coefs*vols;
taus_min= Veff/(co_s*60)
Pmv= 0   #partial pressure in mixed venous blood
Part= 0
rl_shunt= CO*0.1 #right to left shunt as a proportion of CO


stored= np.zeros((0,13)) #initialize storing array

#%%Main loop


while t< 60*duration:
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
    stored= np.vstack((stored, new_data))
    t= t+interval
    if t>60*60:
        Pdel= 1e-10 #almost zero
    
#%% Plot me
figure= plt.figure(figsize=(10,7))
ax= figure.add_subplot(111)


ax.plot(stored[:,0],stored[:,2],color='blue',alpha= 0.5, label='Pcirc')
ax.plot(stored[:,0],stored[:,3],color='yellow',
        lw= 3, label='Palv')
ax.plot(stored[:,0],stored[:,4],color='red', label='Part')
ax.plot(stored[:,0],stored[:,9],color='cyan',
        lw=3, label='Pcns')
ax.plot(stored[:,0],stored[:,-2],color='#a2142f', label='Pfat')

ax.set_xlabel( 'Time(min)')
ax.set_ylabel('drug(%)')
xticks= np.arange(0,duration*60,600)
ax.set_xticks(xticks)
ax.set_xticklabels(xticks/60)
ax.grid()
ax.legend()
ax.set_title(f'Uptake and distribution of {drug}. Millers model')

plt.show()