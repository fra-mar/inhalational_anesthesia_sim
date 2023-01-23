

import numpy as np
from matplotlib import pyplot as plt

import matplotlib.animation as animation


#%%Figure for animation
fig= plt.figure() 
ax= fig.add_subplot(111)

xs=np.linspace(0,2*np.pi,200)
l,= ax.plot(xs, np.sin(xs))
temp= 0
def update(i):
    global temp
    temp= temp+1
    print (temp)
    l.set_ydata(np.sin((xs+i/10)))
    return l,

ani=animation.FuncAnimation(fig,update,200,interval=25,blit=False)



