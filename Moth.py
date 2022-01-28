from Classes.CalculationClass import simulation, timeit
from Classes.viewer import reader
import sys
import os
from termcolor import colored
import importlib.util
from Classes.logo import *





try:
    addr=os.getcwd()+"/"+sys.argv[1]
    target=sys.argv[2]
    print(addr)
    spec = importlib.util.spec_from_file_location("configs", addr)
    configs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(configs)
except ImportError:
    sys.exit(colored("Something is wrong with the name or location of the config file",'red'))

@timeit
def Simulation():
    print(logo)
    S=simulation(DeleteFlag             =   True,
                 DescendingCoefficient  =   2,
                 PathToFolder           =   configs.FolderName,
                 StructureParameters    =   configs.StructureParameters,
                 StructureExchange      =   configs.MaterialExchange,
                 LongRangeExchange      =   configs.LongRangeExchange,
                 NumberOfIterationM     =   50,
                 NumberOfIterationTheta =   1,
                 NumberOfSteps          =   configs.NumberOfSteps,
                 Acceleration           =   configs.Acceleration)
    S.mode(Debug=False)
    #uncomment below to reject previous results
    #S.UsePresolvedResults=False
    if target=="CPU" or target is None:
        file,results=S.GetMHvsT_CPU(Hmin            =   configs.Hmin,
                            Hmax            =   configs.Hmax,
                            Hsteps          =   configs.Hsteps,
                            Tmin            =   configs.Tmin,
                            Tmax            =   configs.Tmax,
                            Tsteps          =   configs.Tsteps,
                            FieldDirection  =   configs.FieldDirection)
    else:
        file,results=S.GetMHvsT_CUDA(Hmin            =   configs.Hmin,
                            Hmax            =   configs.Hmax,
                            Hsteps          =   configs.Hsteps,
                            Tmin            =   configs.Tmin,
                            Tmax            =   configs.Tmax,
                            Tsteps          =   configs.Tsteps,
                            FieldDirection  =   configs.FieldDirection)
    S.dump(file,results)
    data=reader(file)
    data.GetMHonT()
    data.GetMTonH()

Simulation()
