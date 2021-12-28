from MLClass import multilayer
import multiprocessing
from joblib import Parallel, delayed
import os
import numpy as np
from pathlib import Path
import shutil
from os import listdir
from os.path import isfile, join
from functools import wraps
import time
import psutil
from datetime import datetime
import json



def timeit(my_func):
    @wraps(my_func)
    def timed(*args, **kw):
    
        tstart = time.time()
        output = my_func(*args, **kw)
        tend = time.time()
        
        print('"{}" took {:.3f} min to execute\n'.format(my_func.__name__, (tend - tstart)/60))
        return output
    return timed

class simulation:
    def __init__(self,DeleteFlag=True,PathToFolder="temp",StructureParameters={},StructureExchange={},LongRangeExchange="none",NumberOfIterationM=35,NumberOfIterationTheta=100,NumberOfSteps=5000, DescendingCoefficient=0.02):
        self.StructureParameters=StructureParameters
        self.StructureExchange=StructureExchange
        self.LongRangeExchange= LongRangeExchange
        self.PathToFolder = PathToFolder
        self.PathToFolderMH=self.PathToFolder+"-MH"
        self.PathToFolderMT=self.PathToFolder+"-MT"
        self.NumberOfIterationTheta= NumberOfIterationTheta
        self.NumberOfSteps= NumberOfSteps
        self.NumberOfIterationM= NumberOfIterationM
        self.DescendingCoefficient= DescendingCoefficient
        self.num_cores = multiprocessing.cpu_count()
        if DeleteFlag:
            if os.path.exists(self.PathToFolder) and os.path.isdir(self.PathToFolder):
                shutil.rmtree(self.PathToFolder)
            if os.path.exists(self.PathToFolderMH) and os.path.isdir(self.PathToFolderMH):
                shutil.rmtree(self.PathToFolderMH)
            if os.path.exists(self.PathToFolderMT) and os.path.isdir(self.PathToFolderMT):
                shutil.rmtree(self.PathToFolderMT)
        Path(self.PathToFolder).mkdir(parents=True, exist_ok=True)
        Path(self.PathToFolderMH).mkdir(parents=True, exist_ok=True)
        Path(self.PathToFolderMT).mkdir(parents=True, exist_ok=True)

    
    def GetMvsT(self,Tmin=1,Tmax=300,Tsteps=30,Hext=0.1):
        temperature=np.linspace(Tmin,Tmax,Tsteps)
        text="M(T)_profile"
        Parallel(n_jobs=self.num_cores)(delayed(self.minimize)(TargetFolder=self.PathToFolderMT,Field=Hext,FieldDirection=0,Temperature=t,text=text) for t in temperature)
        return 0

    def mode(self,Debug=False):
        if Debug:
            self.num_cores=1
        else:
            self.num_cores = multiprocessing.cpu_count()

    #*****************************************
    def GetMHvsT(self,Hmin=-0.1,Hmax=0.1,Hsteps=32,Tmin=1, Tmax=1, Tsteps=32,FieldDirection=0.0001):
        field       =   np.linspace(Hmin,Hmax,Hsteps)
        Temperature =   np.linspace(Tmin,Tmax,Tsteps)
        result={}
        text="M(H)_profile"
        data=Parallel(n_jobs=self.num_cores)(delayed(self.minimize)(TargetFolder=self.PathToFolderMH,Field=h,FieldDirection=FieldDirection,Temperature=t,text=text) for h in field for t in Temperature)
        keys=list()
        for i in range(len(data)):
            CurrentKey=list(data[i].keys())[0]
            if CurrentKey not in keys:
                keys.append(CurrentKey)
        tmp={}
        for i in range(len(keys)):
            tmp.update({keys[i]:{}})
        for element in data:
            for Tkey in keys:
                if Tkey in list(element.keys()):
                    for Hkey in list(element[Tkey].keys()):
                        tmp[Tkey][Hkey]=element[Tkey][Hkey]
        result=tmp
        result["Hmin"]      =   Hmin
        result["Hmax"]      =   Hmax
        result["Hsteps"]    =   Hsteps
        result["Tmin"]      =   Tmin
        result["Tmax"]      =   Tmax
        result["Tsteps"]    =   Tsteps
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d--%H-%M-%S")
        filename=self.PathToFolder+" results "+current_time+".json"
        with open(filename, 'w') as fout:
            json.dump(result, fout)
        return filename
        
 


    def ProcessMvsT(self,TargetFolder):
        CurrentFolder=os.getcwd()
        mypath=os.path.join(CurrentFolder,TargetFolder)
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        T=np.zeros(len(onlyfiles))
        M=np.zeros(len(onlyfiles))
        Mabs=np.zeros(len(onlyfiles))
        for i,file in enumerate(onlyfiles):
            T[i]=float(file.split("T=")[1].split("_")[0])
            data=np.loadtxt(os.path.join(TargetFolder,file))
            t=data[:,2]
            m=data[:,1]
            M[i]=np.average(m*np.cos(np.radians(t)))
            Mabs[i]=np.average(m)
        SortingIndex=np.argsort(T)
        T=T[SortingIndex]
        M=M[SortingIndex]
        Mabs=Mabs[SortingIndex]
        self.SaveToFileShort(TargetFolder,Filename="M-vs-T",DataX=T,DataY=M,DataZ=Mabs)
    
    def ProcessMvsH(self,TargetFolder):
        CurrentFolder=os.getcwd()
        mypath=os.path.join(CurrentFolder,TargetFolder)
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        H=np.zeros(len(onlyfiles))
        M=np.zeros(len(onlyfiles))
        theta=np.zeros(len(onlyfiles))
        for i,file in enumerate(onlyfiles):
            H[i]=float(file.split("H=")[1].split("_")[0])
            data=np.loadtxt(os.path.join(TargetFolder,file))
            m=data[:,1]
            t=data[:,2]
            M[i]=np.average(m*np.cos(np.radians(t)))
        SortingIndex=np.argsort(H)
        H=H[SortingIndex]
        M=M[SortingIndex]
        self.SaveToFileShort(TargetFolder,Filename="M-vs-H",DataX=H,DataY=M)

        

    def minimize(self,Field=0.1,FieldDirection=0,Temperature=1,text="profile",TargetFolder="tmp"):
        system=multilayer(MaterialParameters=self.StructureParameters,
                          MaterialExchange=self.StructureExchange,
                          LongRangeExchange=self.LongRangeExchange,
                          Temperature=Temperature,
                          Field=Field,
                          FieldDirection=FieldDirection) #init system
        system.InitCalculation(self.NumberOfIterationM,self.NumberOfIterationTheta,self.NumberOfSteps,self.DescendingCoefficient)
        system.SetExternalParameters(Field,FieldDirection,Temperature)
        Plist=list()
        for proc in psutil.process_iter():
            processName = proc.name()
            processID = proc.pid
            if len(processName.split("ython"))>1:
                Plist.append(processID)
        thread=int(np.where(np.array(Plist)==system.pid)[0])
        system.IterateSystem()
        self.SaveToFile(TargetFolder=TargetFolder,strA="H",A=Field,strB="T",B=Temperature,string=text,space=system.space,moment=system.M,angle=system.ThetaM)
        data=self.GrabData(SystemInstance=system,Temperature=Temperature,Field=Field)
        del system
        return data

    def GrabData(self,SystemInstance:multilayer,Temperature, Field):
        Tname       =   "T="+str(round(Temperature, 2))
        Hname       =   "H="+str(round(Field,6))
        space       =   np.double(SystemInstance.space).tolist()
        moment      =   np.double(SystemInstance.M).tolist()
        angle       =   np.double(SystemInstance.ThetaM).tolist()
        LayerNumber =   np.double(SystemInstance.LayerNumber).tolist()
        composition =   SystemInstance.MaterialName.tolist()

        SimulationData  =   {
                                "space":space,
                                "M":moment,
                                "Theta":angle,
                                "MaterialName":composition,
                                "LayerNumber":LayerNumber
                            }
        MonH    ={Hname:SimulationData}
        result  ={Tname: MonH}
        return result



    def SaveToFileShort(self,Folder,Filename, DataX,DataY,DataZ="empty"):
        Filename=Filename+".txt"
        path = os.path.join(Folder,Filename)
        if type(DataZ)==type("empty"):
            e=np.stack((DataX, DataY), axis=-1)
        else:
            e=np.stack((DataX, DataY, DataZ), axis=-1)
        np.savetxt(path, e, fmt='%.18e')
        return 0

    def SaveToFile(self,TargetFolder,strA,A,strB,B,string,space,moment,angle):
        name=strA+"="+str(round(A, 6))+"_"+strB+"="+str(round(B, 2))+"_"+string+".txt"
        path = os.path.join(TargetFolder,name)
        e=np.stack((space, moment, angle), axis=-1)
        np.savetxt(path, e, fmt='%.18e')
        return 0
