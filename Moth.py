from Classes.CalculationClass import simulation, timeit
from Classes.viewer import reader
import sys
import os
from termcolor import colored
import importlib.util
from Classes.logo import *





try:
    addr=os.getcwd()+"/"+sys.argv[1]
    try:
        target=sys.argv[2]
    except:
        terget=None
    spec = importlib.util.spec_from_file_location("configs", addr)
    configs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(configs)
except ImportError:
    sys.exit(colored("Something is wrong with the name or location of the config file",'red'))

@timeit
def Simulation():
    print(logo)
    DeleteFlag=True
    try:
        DeleteFlag=configs.DeleteFlag
    except AttributeError:
        DeleteFlag=True
    S=simulation(DeleteFlag             =   DeleteFlag,
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
    S.UsePresolvedResults=configs.ReusePreviousResults
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
