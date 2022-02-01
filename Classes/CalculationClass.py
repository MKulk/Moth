from Classes.MLClass import multilayer
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
from termcolor import colored

try:
    from numba import jit
    numba_imported=True
except ImportError:
    print("no JIT for today")
    numba_imported=False



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
    def __init__(self,DeleteFlag=True,PathToFolder="temp",StructureParameters={},StructureExchange={},
                 LongRangeExchange="none",NumberOfIterationM=35,NumberOfIterationTheta=100,NumberOfSteps=5000,
                 DescendingCoefficient=0.02, Acceleration=1.5):
        self.StructureParameters=StructureParameters
        self.StructureExchange=StructureExchange
        self.LongRangeExchange= LongRangeExchange
        self.PathToFolder = PathToFolder
        self.UsePresolvedResults=True
        #self.PathToFolderMH=self.PathToFolder#+"-MH"
        #self.PathToFolderMT=self.PathToFolder+"-MT"
        self.NumberOfIterationTheta= NumberOfIterationTheta
        self.NumberOfSteps= NumberOfSteps
        self.NumberOfIterationM= NumberOfIterationM
        self.DescendingCoefficient= DescendingCoefficient
        self.Acceleration= Acceleration
        now = datetime.now()
        self.current_time = now.strftime("%Y-%m-%d--%H-%M-%S")
        self.num_cores = multiprocessing.cpu_count()
        if DeleteFlag:
            if os.path.exists(self.PathToFolder) and os.path.isdir(self.PathToFolder):
                shutil.rmtree(self.PathToFolder)
        Path(self.PathToFolder).mkdir(parents=True, exist_ok=True)

    
    #def GetMvsT(self,Tmin=1,Tmax=300,Tsteps=30,Hext=0.1):
    #    temperature=np.linspace(Tmin,Tmax,Tsteps)
    #    text="M(T)_profile"
    #    Parallel(n_jobs=self.num_cores)(delayed(self.minimize)(TargetFolder=self.PathToFolderMT,Field=Hext,FieldDirection=0,Temperature=t,text=text) for t in temperature)
    #    return 0

    def mode(self,Debug=False):
        if Debug:
            self.num_cores=1
        else:
            self.num_cores = multiprocessing.cpu_count()

    #*****************************************
    def GetMHvsT_CPU(self,Hmin=-0.1,Hmax=0.1,Hsteps=32,Tmin=1, Tmax=1, Tsteps=32,FieldDirection=0.0001):
        self.field       =   np.linspace(Hmin,Hmax,Hsteps)
        self.Temperature =   np.linspace(Tmin,Tmax,Tsteps)
        result={}
        text="M(H)_profile"
        data=Parallel(n_jobs=self.num_cores)(delayed(self.minimize)(TargetFolder=self.PathToFolder,
                                                                    Field=h,FieldDirection=FieldDirection,
                                                                    Temperature=t,text=text,iH=i,iT=j) 
                                             for i,h in enumerate(self.field) 
                                             for j,t in enumerate(self.Temperature))
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
        filename=self.PathToFolder+" "+self.current_time+".json"
        return filename,result
    if numba_imported is True:
        @jit()#lol of course this will not work
        def GetMHvsT_CUDA(self,Hmin=-0.1,Hmax=0.1,Hsteps=32,Tmin=1, Tmax=1, Tsteps=32,FieldDirection=0.0001):
            self.field       =   np.linspace(Hmin,Hmax,Hsteps)
            self.Temperature =   np.linspace(Tmin,Tmax,Tsteps)
            result={}
            text="M(H)_profile"
            data=[]
            for h in self.field:
                for t in self.Temperature:
                    data.append(self.minimize(TargetFolder=self.PathToFolder,Field=h,FieldDirection=FieldDirection,Temperature=t,text=text))
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
            filename=self.PathToFolder+" "+self.current_time+".json"
            return filename,result
    else:
        print("GPU computation is not supported")
 

    def dump(self,filename,data):
        with open(filename, 'w') as fout:
            json.dump(data, fout)
            
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

    def minimize(self,Field=0.1,FieldDirection=0,Temperature=1,text="M(H)_profile",TargetFolder="tmp", demo=False,iH=0,iT=0):
        MPresolved,ThetaPresolved=self.GetPreviousResult(TargetFolder,iH,iT, text)
        self.system=multilayer(MaterialParameters=self.StructureParameters,
                          MaterialExchange=self.StructureExchange,
                          LongRangeExchange=self.LongRangeExchange,
                          Temperature=Temperature,
                          Field=Field,
                          FieldDirection=FieldDirection,
                          Acceleration=self.Acceleration) #init system
        self.system.InitCalculation(NumberOfIterationM=self.NumberOfIterationM,
                                    NumberOfIterationTheta=self.NumberOfIterationTheta,
                                    NumberOfSteps=self.NumberOfSteps,
                                    DescendingCoefficient=self.DescendingCoefficient,
                                    PresolvedM=MPresolved,
                                    PresolvedTheta=ThetaPresolved)
        self.system.SetExternalParameters(Field,FieldDirection,Temperature)
        if demo is not True:
            self.system.IterateSystem()
            self.SaveToFile(TargetFolder=TargetFolder,strA="H",A=Field,strB="T",
                            B=Temperature,string=text,space=self.system.space,
                            moment=self.system.M,angle=self.system.ThetaM)
            data=self.GrabData(SystemInstance=self.system,Temperature=Temperature,Field=Field)
            #del self.system
        else:
            data=0
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
        path,name=self.CreateName(TargetFolder,strA,A,strB,B,string)
        e=np.stack((space, moment, angle), axis=-1)
        np.savetxt(path, e, fmt='%.18e')
        return 0
    def CreateName(self,TargetFolder,strA,A,strB,B,string):
        name=strA+"="+str(round(A, 6))+"_"+strB+"="+str(round(B, 2))+"_"+string+".txt"
        path = os.path.join(TargetFolder,name)
        return path, name
    
    def GetPreviousResult(self,TargetFolder,iH,iT,text):
        CurrentFolder=os.getcwd()
        SolutionsFolder=os.path.join(CurrentFolder,TargetFolder)
        SolutionFiles = [f for f in listdir(SolutionsFolder) if isfile(join(SolutionsFolder, f))]
        neighboursH=np.array([0,-1,0,-1,-2,0,-2,-1,-2])
        neighboursT=np.array([0,0,-1,-1,0,-2,-1,-2,-2])
        nH=iH+neighboursH
        nT=iT+neighboursT
        nH[nH<0]=0
        nT[nT<0]=0
        Names=[]
        for i in range(nH.size):
            path, name = self.CreateName(TargetFolder=TargetFolder,strA="H",A=self.field[nH[i]],strB="T",B=self.Temperature[nT[i]],string=text)
            if name in SolutionFiles:
                Names.append(name)
        if Names and self.UsePresolvedResults:
            Solution=Names[0]
            data=np.loadtxt(os.path.join(TargetFolder,Solution))
            Mpresolved=data[:,1]
            ThetaPresolved=data[:,2]
            print(colored("The previously calculated data is going to be used: "+Solution,"yellow"))
        else:
            Mpresolved=None
            ThetaPresolved=None
        
        
        #H=np.zeros(len(onlyfiles))
        #M=np.zeros(len(onlyfiles))
        #theta=np.zeros(len(onlyfiles))
        #for i,file in enumerate(onlyfiles):
        #    H[i]=float(file.split("H=")[1].split("_")[0])
        #    data=np.loadtxt(os.path.join(TargetFolder,file))
        #    m=data[:,1]
        #    t=data[:,2]
        #    M[i]=np.average(m*np.cos(np.radians(t)))
        #SortingIndex=np.argsort(H)
        #H=H[SortingIndex]
        #M=M[SortingIndex]
        #self.SaveToFileShort(TargetFolder,Filename="M-vs-H",DataX=H,DataY=M)

        return Mpresolved,ThetaPresolved