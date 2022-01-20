
from CalculationClass import simulation, timeit
from viewer import reader
import sys
import os
from termcolor import colored
import importlib.util




try:
    addr=os.getcwd()+"/"+sys.argv[1]
    print(addr)
    spec = importlib.util.spec_from_file_location("configs", addr)
    configs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(configs)
except ImportError:
    sys.exit(colored("Something is wrong with the name or location of the config file",'red'))

@timeit
def Simulation():
    S=simulation(DeleteFlag             =   True,
                 DescendingCoefficient  =   2,
                 PathToFolder           =   configs.FolderName,
                 StructureParameters    =   configs.StructureParameters,
                 StructureExchange      =   configs.MaterialExchange,
                 LongRangeExchange      =   configs.LongRangeExchange,
                 NumberOfIterationM     =   50,
                 NumberOfIterationTheta =   1,
                 NumberOfSteps=60)
    S.mode(Debug=False)
    file=S.GetMHvsT(
                    Hmin            =   configs.Hmin,
                    Hmax            =   configs.Hmax,
                    Hsteps          =   configs.Hsteps,
                    Tmin            =   configs.Tmin,
                    Tmax            =   configs.Tmax,
                    Tsteps          =   configs.Tsteps,
                    FieldDirection  =   configs.FieldDirection)
    data=reader(file)
    data.GetMHonT()
    data.GetMTonH()

Simulation()
