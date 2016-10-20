
from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np

def TEMP2RES(T):
        return 100*(1+ 3.908e-3*T - 5.775e-7*T**2 + (0 if T > 0 else -4.183e-12)*(T-100)**3 )

#X = np.arange(-200, 100, .1)
#Y = list(map(TEMP2RES, X))
#p = np.polyfit(X,Y,2)
#print(p)
#fit = np.poly1d(p)
#plt.plot(X, abs(fit(X)-Y))

# this polynomial fits the above equation with 10e-5 accuracy
def temp2res(t):
    return -5.75599079e-05*(t**2) + 3.90784802e-01*t + 1.00000128e+02


def RES2TEMP(r):
    measure=r
    inf=-200; sup=850 ; temp=0; essai=100
    while abs(measure-essai) > 0.001:
        #print(measure, temp, essai, inf, sup)
        if essai>measure:
            sup=temp
        else:
            inf=temp
        temp=(sup+inf)/2.0
        essai=temp2res(temp)
    #print(temp)
    return temp
    
#X = np.arange(20, 140, .1)
#Y = [RES2TEMP(x) for x in X]
#p = np.polyfit(X,Y,3)
#print(p)
#fit = np.poly1d(p)
#plt.plot(X, abs(fit(X)-Y))

#this polynomial fits the above function with a 4e10-3 accuracy
def res2temp(r):
    return 6.76101314e-07*(r**3) + 7.62125457e-04*(r**2) + 2.38630456e+00*r - 2.46928114e+02
    #return 7.62125457e-04*(r**2) + 2.38630456e+00*r - 2.46928114e+02
    
# temp -200 100
# res   20  140
X = np.arange(-200, 100, .1)
Y = res2temp(temp2res(X))
plt.plot(X, abs(X-Y))
plt.show()
