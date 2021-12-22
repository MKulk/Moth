import numpy as np
import math

MaterialName=["F1","F1","F1","F1","F1","F1","F1","F1","F2","F2","F2","F2","F2","F2","F2","F2","F1","F1","F1","F1","F1","F1","F1","F1","F2","F2","F2","F2"]
MaterialName=np.array(MaterialName)
LayerNumber= [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3]
MLThickness=[0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15]
MLPosition=np.cumsum(MLThickness)


#New parameter
ExchangeLength=[0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,1.5,1.5,1.5,1.5]
ExchangeLength=np.array(ExchangeLength)*0.2
M=np.ones_like(ExchangeLength)*0.8
Theta=np.sin(np.arange(M.size)*3.14/180)
#length of the tail
#exchnange pairs
JJ={
    "F1-F2":10,
    "F2-F1":10,
    "":0
}

Jp=np.zeros((MaterialName.size,MaterialName.size),dtype=float)
Jm=np.zeros((MaterialName.size,MaterialName.size),dtype=float)

Np=np.zeros((MaterialName.size,MaterialName.size),dtype=np.str_)
Nm=np.zeros((MaterialName.size,MaterialName.size),dtype=np.str_)

#Generate
expP=np.zeros((MaterialName.size,MaterialName.size),dtype=float)
expM=np.zeros((MaterialName.size,MaterialName.size),dtype=float)
patternP=np.zeros(MaterialName.size,dtype=float)
patternM=np.zeros(MaterialName.size,dtype=float)

index=-1
delta=-1
for i in range (MaterialName.size):
    if index-LayerNumber[i]==-1:
        z=-delta*MLThickness[i]
        patternP[i]=math.e**(z/ExchangeLength[i])
        delta+=1
    else:
        delta=-1
        z=-delta*MLThickness[i]
        patternP[i]=math.e**(z/ExchangeLength[i])
        delta+=1
        index+=1
index=-1
delta=-1
for i in range (MaterialName.size):
    if index-LayerNumber[i]==-1:
        z=-delta*MLThickness[i]
        patternP[i]=math.e**(z/ExchangeLength[i])
        delta+=1
    else:
        delta=-1
        z=-delta*MLThickness[i]
        patternP[i]=math.e**(z/ExchangeLength[i])
        delta+=1
        index+=1
index=LayerNumber[-1]+1
delta=-1
for i in reversed(range (MaterialName.size)):
    if index-LayerNumber[i]==1:
        z=-delta*MLThickness[i]
        patternM[i]=math.e**(z/ExchangeLength[i])
        delta+=1
    else:
        delta=-1
        z=-delta*MLThickness[i]
        patternM[i]=math.e**(z/ExchangeLength[i])
        delta+=1
        index+=1

for i in range (MaterialName.size):
    print(MLPosition[i], patternM[i])
#expL=np.tril(exp, -1)
#expU=np.triu(exp, 1)
def flip(a):
   b=np.zeros_like(a)
   for i in range(a[0].size):
       for j in range(a[0].size):
           b[j,i] = a[i,j]
   return b
#xpUL=flip(expU)
#xpd=expUL*expL
#xpD=expd+flip(expd)
#ask=(exp!=0)*1
#exp[exp<0.03]=0#cutoff
#for k in range(MaterialName.size):
#    for i in range (MaterialName.size):
#        print(MLPosition[i], k, expD[k,i])
#left to right scan