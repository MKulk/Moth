import numpy as np
import json


class reader():
    def __init__(self,filename=None):
        with open(filename, 'r') as fin:
            self.data=json.load(fin)
        self.filename       =   filename.split(".json")[0]
        self.Tmin           =   self.data["Tmin"]
        self.Tmax           =   self.data["Tmax"]
        self.Tsteps         =   self.data["Tsteps"]
        self.Hmin           =   self.data["Hmin"]
        self.Hmax           =   self.data["Hmax"]
        self.Hsteps         =   self.data["Hsteps"]
        self.Tarray         =   np.linspace(self.Tmin,self.Tmax,self.Tsteps)
        self.Harray         =   np.linspace(self.Hmin,self.Hmax,self.Hsteps)
        
    def GetMHonT(self):
        Mx      =       np.zeros((self.Hsteps,self.Tsteps+1))
        My      =       np.zeros((self.Hsteps,self.Tsteps+1))
        Ma      =       np.zeros((self.Hsteps,self.Tsteps+1))
        for i,h in enumerate(self.Harray):
            for j,t in enumerate(self.Tarray):
                Tkey        =   "T="+str(round(t,2))
                Hkey        =   "H="+str(round(h,6))
                M           =   np.array(self.data[Tkey][Hkey]["M"])
                Theta       =   np.array(self.data[Tkey][Hkey]["Theta"])
                Mx[i,j+1]   =   np.average(M*np.cos(np.radians(Theta)))
                My[i,j+1]   =   np.average(M*np.sin(np.radians(Theta)))
                Ma[i,j+1]   =   np.average(M)
        Mx[:,0]     =   self.Harray
        My[:,0]     =   self.Harray
        Ma[:,0]     =   self.Harray
        header="H"
        for t in self.Tarray:
            header=header+" "+"T="+str(round(t,2))
        np.savetxt(self.filename+"_Mx_vs_H"+".txt", Mx, delimiter=' ', header=header,comments='')
        np.savetxt(self.filename+"_My_vs_H"+".txt", My, delimiter=' ', header=header,comments='')
        np.savetxt(self.filename+"_Ma_vs_H"+".txt", Ma, delimiter=' ', header=header,comments='')
    def GetMTonH(self):
        Mx      =       np.zeros((self.Tsteps,self.Hsteps+1))
        My      =       np.zeros((self.Tsteps,self.Hsteps+1))
        Ma      =       np.zeros((self.Tsteps,self.Hsteps+1))
        for i,t in enumerate(self.Tarray):
            for j,h in enumerate(self.Harray):
                Tkey        =   "T="+str(round(t,2))
                Hkey        =   "H="+str(round(h,6))
                M        =   np.array(self.data[Tkey][Hkey]["M"])
                Theta       =   np.array(self.data[Tkey][Hkey]["Theta"])
                Mx[i,j+1]   =   np.average(M*np.cos(np.radians(Theta)))
                My[i,j+1]   =   np.average(M*np.sin(np.radians(Theta)))
                Ma[i,j+1]   =   np.average(M)
        Mx[:,0]     =   self.Tarray
        My[:,0]     =   self.Tarray
        Ma[:,0]     =   self.Tarray
        header="T"
        for h in self.Harray:
            header=header+" "+"H="+str(round(h,3))
        np.savetxt(self.filename+"_Mx_vs_T"+".txt", Mx, delimiter=' ', header=header,comments='')
        np.savetxt(self.filename+"_My_vs_T"+".txt", My, delimiter=' ', header=header,comments='')
        np.savetxt(self.filename+"_Ma_vs_T"+".txt", Ma, delimiter=' ', header=header,comments='')
    
if __name__ == "__main__":
    import os
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        a=f.split(".json")
        if len(a)>1:
            filename=f
            data=reader(filename)
            data.GetMTonH()