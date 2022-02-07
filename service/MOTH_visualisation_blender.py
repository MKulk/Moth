#import bpy


from os import listdir
from os.path import isfile, join
import os
import numpy as np
def get_parameters(path):
        filenames = [f for f in listdir(path) if isfile(join(path, f))]
        fields=[]
        temps=[]
        for i,name in enumerate(filenames):
            h=float(name.split("H=")[1].split("_")[0])
            fields.append(h)
            t=float(name.split("T=")[1].split("_")[0])
            temps.append(t)
            print(compose_name(h,t)==name)
        fields=np.sort(np.unique(np.array(fields)))
        temps=np.sort(np.unique(np.array(temps)))
        s,m,o=read_state(path+os.path.sep+filenames[0])
        number_of_layers=s.size
        return fields,temps,number_of_layers 
def compose_name(field_i,temp_i):
    name="H="+str(field_i)+"_T="+str(temp_i)+"_M(H)_profile.txt"
    return name
def read_state(path_to_file):
    data=np.loadtxt(path_to_file)
    space, magnitude, angle = data[:,0],data[:,1],data[:,2]
    return space,magnitude,angle
    




path="C:\Dropbox\KTH data\WIP\high priority\Layered Model bare system\Multilayer-simulation\CS_L=0.15nm_J=1proc"
get_parameters(path)