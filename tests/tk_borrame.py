import tkinter as tk
from tkinter import ttk

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation

root= tk.Tk()
root.title('Testing, as usual')

width= 800
w= root.winfo_screenwidth()
m= int((w-900)/2)
s= tk.DoubleVar() #for the slide bar

root.geometry(f'{width}x600+{m}+100')

#%%Create two canvas
t_canvas= tk.Canvas(master=root,bg='#af23ab')
t_canvas.place(relwidth=0.48, relheight=1.0, relx=0,rely=0)

i_canvas=tk.Canvas(master=root)#, bg='white')
i_canvas.place(relwidth=0.52, relheight=0.3, relx=0.5,rely=0)

fig= plt.Figure()
an_canvas = FigureCanvasTkAgg(fig, master=root)
an_canvas.get_tk_widget().place(relx=0.5, 
                                rely=0.31,
                                relheight=0.69,
                                relwidth= 0.52)

#%%Create twolbels in t_canvas
label1= ttk.Label(t_canvas, text="meeeee", background= '#af23ab')
label2= ttk.Label(t_canvas, text="a un agujero")

label1.place(relx= 0.2,rely=0.2)
label2.place(relx= 0.2, rely=0.8)


#%%Create and action if <Escape> pressed
def printthis(a):
    print('You pressed Escape!')

    
root.bind('<Escape>', printthis)

#%%Create an slider in i_canvas

'''
Looks like you DEFINE a variable (s= tk.DoubleVar(), look at the beginning)
The argument variable in ttk.Scale puts the value in the variable.
Then you "call" that variable with slide.get()

'''
def slider_change(event):
    s= slider.get()
    label2['text']= f'{slider.get():.2f}'
    print(float(s))
slider= ttk.Scale(t_canvas,from_=10,to=0, 
                  orient= 'vertical',
                  variable= s,
                  command= slider_change)
slider.place(relx=0.5, rely=0.2,relheight=0.6)
label2['text']= f'{slider.get():.2f}'

#%%
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
Pheart, Pkidney, Pliver, Pcns, Pmuscle, Pfat, Pvrg= 0,0,0,0,0,0,0
 

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
#%%Figure for animation
#fig was defined when canvas was defined
ax= fig.add_subplot(111)

xs=np.linspace(0,2*np.pi,200)
l,= ax.plot(xs, np.sin(xs))

def update(i):
    
    global t, sto, Pdel, Ppulm, Pcirc, Palv, Pmv, new_data
    global Part, Pheart, Pkidney, Pliver, Pcns, Pfat, Pvrg, Pmuscle
    Pheart= Pheart+0.02
    sto= np.vstack((sto,np.zeros(13)))
    l.set_ydata(np.sin((xs+i/10)))
    return l,

ani=animation.FuncAnimation(fig,update,np.arange(0,200),interval=25,blit=False)

root.mainloop()

