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

#%%Figure for animation
#fig was defined when canvas was defined
ax= fig.add_subplot(111)

xs=np.linspace(0,2*np.pi,200)
l,= ax.plot(xs, np.sin(xs))
def update(i):
    l.set_ydata(np.sin((xs+i/10)))
    return l,

ani=animation.FuncAnimation(fig,update,np.arange(0,200),interval=25,blit=False)

root.mainloop()

