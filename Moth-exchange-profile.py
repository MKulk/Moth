from Classes.CalculationClass import simulation, timeit
from Classes.viewer import reader
import sys
import os
from termcolor import colored
import importlib.util
from Classes.logo import *





try:
    addr=os.getcwd()+os.path.sep+sys.argv[1]
    print(addr)
    spec = importlib.util.spec_from_file_location("configs", addr)
    configs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(configs)
except ImportError:
    sys.exit(colored("Something is wrong with the name or location of the config file",'red'))

def GetExchangeProfile():
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
    S.minimize(demo=True)
    original_stdout = sys.stdout
    with open(os.getcwd()+os.path.sep+os.path.sep+configs.FolderName+'_profile.txt', 'w') as f:
        sys.stdout = f
        for i in range(S.system.B.size):
            for j in range(S.system.B.size):
                print(i, j, S.system.NeighboursWeight[i,j])
        sys.stdout = original_stdout

GetExchangeProfile()
