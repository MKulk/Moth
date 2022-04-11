import numpy as np
import sys
import matplotlib.pyplot as plt
from scipy import optimize

input="C:\Dropbox\KTH data\WIP\high priority\Direct observation of MC effect\Moth_sim\CS-search\CS_L=4.0_J=2_proc-directx1.5-prec 2022-03-13--18-50-59_Ma_vs_H.txt"
with open(input) as f:
    header = f.readline().rstrip().split(' ')

T_points=len(header)-1
names=header[1:]
print(names)
data = np.loadtxt(input, delimiter=' ', skiprows=1)
H_data=data[:,0]
print(H_data)
H_points=data[:,0].size
print(H_points)

def fit_func(x, a, c, k):
    return k+a*np.sin(x*6.28 - c)

def swipe(data,Tindex=0, nHDCmin=0, nHDCmax=96, nHACmin=1, nHACmax=20,name=""):
    #HAC is in unit of amplitude and not not peak-peak
    with open(name+".txt", 'w') as f:
        for i in range(nHDCmax):
            for j in range(nHACmax-1):
                nHAC=j+1
                nHDC=i
                if nHDC-nHAC>0 and nHDC+nHAC<nHDCmax:
                    Hstart=nHDC-nHAC
                    Hstop=nHDC+nHAC
                    piece=data[Hstart:Hstop+1,Tindex+1]
                    signal=np.concatenate((piece, np.flip(piece,0)), axis=0)
                    #plt.figure()
                    #plt.clf()
                    x=np.linspace(0,1,signal.size)
                    #plt.scatter(x, signal , color='black', zorder=20, label='Data')
                    params, params_covariance = optimize.curve_fit(fit_func, x, signal)
                    #plt.plot(x, fit_func(x, params[0], params[1], params[2]), label='Fitted function')
                    #plt.show()
                    #print(np.abs(H_data[nHDC]-H_data[nHDC+nHAC])*2,H_data[nHDC],params[0],file=f)
                    h=np.abs(H_data[0]-H_data[np.abs(nHAC)*2])
                    #np.abs(nHAC)*2
                    print(H_data[nHDC]*10000, h*10000 ,np.abs(params[0]),params[1],params[2],file=f)
    return piece
for i in range(len(names)):
    a=swipe(data,Tindex=i,nHDCmin=0, nHDCmax=H_points,nHACmax=30,name=names[i])