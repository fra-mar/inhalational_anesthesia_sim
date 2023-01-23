#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 230105

Animated distrubution model. Embedded in Tkinter

About sim speed and using classes in animations, check out
https://stackoverflow.com/questions/41882736/can-i-change-the-interval-of-a-previously-created-matplotlib-funcanimation
"""
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from inh_pk_data import inh_drugs_data
import tkinter as tk
from tkinter import ttk



#%%Physio and drug data in order: 
#blood(b/g),heart(t/b), kidney, liver, cns, muscle, fat, vrg

pk_data= inh_drugs_data()
drug= 'Halothane'
drug_coefs= pk_data.loc[drug] #load bg and tb partition coefficients
vols= pk_data.loc['vols'] #load compartments volumnes
co_f= pk_data.loc['co_f'] #load fractional cardiac outputs per compartment

Veff= drug_coefs*vols #effective volumes

#%% Initial variables, partial pressures
Pdel= 1e-8  #Vaporizer, initial pressure
Pcirc= 1e-8
Palv= 1e-8
Pheart= 1e-8
Pkidney= 1e-8
Pliver= 1e-8
Pcns=  1e-8
Pmuscle= 1e-8
Pfat= 1e-8 
Pvrg= 1e-8
 

#%%Initial variables, other
t=0
t_0=0; t_f= 3600 #for xticks calculation
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
rl_shunt= CO*0.15 #right to left shunt as a proportion of CO

sto= np.zeros((0,13)) #initialize storing array
paused= False
frame_ms= 20 #frame duration in milliseconds.
#%%Start Tkinter window + create 2 canvas + bind pltFigure 

root= tk.Tk()
root.title(f'Uptake and distribution of {drug}. Millers model')

w= root.winfo_screenwidth()
h= root.winfo_screenmmheight()
width= int(w*0.9)
height= int(w*0.9)
mw= int((w-width)/2)
mh= int((h-height)/2)
root.geometry(f'{width}x{height}+{mw}+{mh}')

t_canvas= tk.Canvas(master=root,bg='#af23ab')
t_canvas.place(relwidth=0.2, relheight=1.0, relx=0,rely=0,
               border='outside')


i_canvas=tk.Canvas(master=root)#, bg='white')
i_canvas.place(relwidth=0.8, relheight=1.0, relx=0.2,rely=0)

figure= plt.Figure(figsize=(7,10))
an_canvas = FigureCanvasTkAgg(figure, master=i_canvas)
an_canvas.get_tk_widget().place(relx=0.005, 
                                rely=0.01,
                                relheight=0.98,
                                relwidth= 0.99)

#%%Create two labels in t_canvas and a slider

#Superior slides labels
label1= ttk.Label(t_canvas, text=f"Vaporizer\n  %{drug}",
                  foreground= 'white',
                  background= '#af23ab')
label1.place(relx= 0.02,rely=0.06)


label2= ttk.Label(t_canvas, text=" FGF\nL/min",
                  foreground= 'white',
                  background= '#af23ab')
label2.place(relx= 0.3,rely=0.06)

label3= ttk.Label(t_canvas, text=" MV\nL/min",
                  foreground= 'white',
                  background= '#af23ab')
label3.place(relx= 0.56,rely=0.06)

label4= ttk.Label(t_canvas, text=" CO\nL/min",
                  foreground= 'white',
                  background= '#af23ab')
label4.place(relx= 0.81,rely=0.06)
#---------------------------------------------

#Inferir slides labels 
label_s_del= ttk.Label(t_canvas, text="")
label_s_del.place(relx= 0.06, rely=0.75)

label_s_fgf= ttk.Label(t_canvas, text="")
label_s_fgf.place(relx= 0.3, rely=0.75)

label_s_minVol= ttk.Label(t_canvas, text="")
label_s_minVol.place(relx= 0.56, rely=0.75)

label_s_CO= ttk.Label(t_canvas, text="")
label_s_CO.place(relx= 0.82, rely=0.75)
#--------------------------------------------
def s_del(event):
    #global Pdel
    #s= slider_del.get()
    label_s_del['text']= f'{slider_del.get():.1f}'
    #Pdel= float(s)

s= tk.DoubleVar() #for the slide bar    
slider_del= ttk.Scale(t_canvas,from_=8,to=1e-5, 
                  orient= 'vertical',
                  variable= s,
                  command= s_del)
slider_del.set(Pdel)
slider_del.place(relx=0.08, rely=0.1,relheight=0.63)

#-----------------------------------

def s_fgf(event):
    #global fgf
    #f= slider_fgf.get()
    label_s_fgf['text']= f'{slider_fgf.get():.1f}'
    #fgf= f/60
    
f= tk.DoubleVar() #for the slide bar    
slider_fgf= ttk.Scale(t_canvas,from_=10,to=1e-5, 
                  orient= 'vertical',
                  variable= f,
                  command= s_fgf)
slider_fgf.set(fgf*60)
slider_fgf.place(relx=0.33, rely=0.1,relheight=0.63)


#-----------------------------------
def s_minVol(event):
    label_s_minVol['text']= f'{slider_minVol.get():.1f}'
    
    
    

v= tk.DoubleVar() #for the slide bar    
slider_minVol= ttk.Scale(t_canvas,from_=10,to=1e-5, 
                  orient= 'vertical',
                  variable= v,
                  command= s_minVol)
slider_minVol.set(V*60)
slider_minVol.place(relx=0.58, rely=0.1,relheight=0.63)

#____________________________________

def s_CO(event):
    label_s_CO['text']= f'{slider_CO.get():.1f}'
    
co= tk.DoubleVar() #for the slide bar    
slider_CO= ttk.Scale(t_canvas,from_=10,to=1e-5, 
                  orient= 'vertical',
                  variable= co,
                  command= s_CO)
slider_CO.set(CO*60)
slider_CO.place(relx=0.83, rely=0.1,relheight=0.63)

#%%Buttons
def new_params():
    global Pdel, fgf, V, Vd, Va, CO, co_s
    s= slider_del.get()
    Pdel= float(s)
    
    f= slider_fgf.get()
    fgf= f/60
    
    v= slider_minVol.get()
    V= float(v)/60
    Vd= V*0.15 #dead space
    Va= V-Vd 
    
    co= slider_CO.get()
    CO= float(co)/60
    co_s= co_f*CO

def paus_res():
    global paused
    if paused== False:
        ani.pause()
    if paused== True:
        ani.resume()
    paused= not paused
    
def exit_b():
    root.destroy()
    arr_to_save= sto[sto[:,0]%10 == 0] #will save just 1/10 points
    header='t, Pdel, Pcirc, Palv, Part, Pmv,Pheart, Pkidney, Pliver, Pcns, Pmuscle, Pfat, Pvrg'
    np.savetxt('sim_data.csv', arr_to_save, delimiter=',',
               header= header)

def acc_b():
    global frame_ms
    if frame_ms > 950:
        pass
    else:
        frame_ms += 50
    print(frame_ms)

def dec_b():
    global frame_ms
    if frame_ms > 80:
        frame_ms -= 50
    else:
        pass
    print(frame_ms)

set_button= ttk.Button(t_canvas, text='SET', command= new_params)
set_button.place(relx= 0.05,rely= 0.8, relwidth= 0.45, relheight=0.04)

pause_button= ttk.Button(t_canvas, text= 'Paus/Resume', command= paus_res)
pause_button.place(relx= 0.5, relwidth= 0.45, rely= 0.8, relheight= 0.04)

exit_button= ttk.Button(t_canvas, text= 'EXIT', command= exit_b)
exit_button.place(relx= 0.05, relwidth= 0.9, rely= 0.95, relheight= 0.04)


dec_button= tk.Button(t_canvas, text='<< Slower', command= acc_b)
dec_button.place(relx= 0.05, relwidth= 0.45, rely= 0.875, relheight= 0.04)

acc_button= tk.Button(t_canvas, text='Faster >>', command= dec_b)
acc_button.place(relx= 0.5, relwidth= 0.45, rely= 0.875, relheight= 0.04)


#%%Start the plot
ax= figure.add_subplot(111)
ax.set_ylim([0,8])

l_circ, = ax.plot([],[],'y-',alpha= 0.5, label='Pcirc')
l_alv, = ax.plot([],[],'b-',alpha= 0.5, label='Palv')
l_art, = ax.plot([],[],'r-', label='Part')
l_cns, = ax.plot([],[],'g-',lw=3, label='Pcns')
l_musc, = ax.plot([],[], 'r-.', label= 'Pmusc')
l_fat, = ax.plot([],[],color= 'r',ls= ':', label='Pfat')

ax.set_xlabel( 'Time(min)')
ax.set_ylabel('drug(%)')

time_text= ax.text(0.75,1.02,'', color= '#2f847c',fontsize= 30, 
        alpha= 0.5,  
        transform= ax.transAxes)

ax.grid()
ax.legend()


#%%Main loop

def time_displayer(t):
    if t//60 < 60:
        return f'{t//60}min {t%60}s'
    else:
        h= t//3600
        m= t//60 - h*60
        s= t - h*3600 - m*60
        return f'{h}h {m}min {s}s'

def gen(): #generates a number of frames if a condition is fullfilled
    global frame_ms
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
    
    t= t+interval
    if t>50*60:
        t_0= t - 3000
        t_f= t-3000+3600
    else:
        t_0= 0
        t_f= 3600
    xticks= np.arange(t_0,t_f)
    xticks= xticks[xticks%600==0]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks/60)
        
    ax.set_xlim([t_0,t_f])
    
    l_circ.set_data(sto[:,0],sto[:,2])
    l_alv.set_data(sto[:,0],sto[:,3])
    l_art.set_data(sto[:,0],sto[:,4])
    l_cns.set_data(sto[:,0],sto[:,9])
    l_musc.set_data(sto[:,0],sto[:,10])
    l_fat.set_data(sto[:,0],sto[:,11])
    
    time_text.set_text(time_displayer(t))
    
    ani.event_source.interval= frame_ms
    
    ax.collections.clear()
    
    return l_circ, l_cns,l_alv, l_art, l_musc, l_fat, 
    
#%% Animation function

ani= FuncAnimation(figure, func= animate,
                   repeat= False,
                   frames= gen,interval= frame_ms,
                              blit=False)

ani.pause()
plt.show()

root.mainloop()