MaterialExchange={
            "FeCr1-FeCr1"   :0.023,
            "FeCr2-FeCr1"   :0.000,
            "FeCr1-FeCr2"   :0.000,
            "FeCr2-FeCr2"   :0.023
            }
RKKYExchange={
            "FeCr2-FeCr1"  :-0.0008,
            "FeCr1-FeCr2"  :-0.0008
            }

FeCr_Parameters={
            "MaterialThickness":(50,),
            "MLThickness":(0.15,),
            "MaterialName":("FeCr1",),
            "MaterialS":(1,),
            "MaterialExtraField":(0,),
            "MaterialExtraFieldDirection":(0,),
            "MaterialSaturationM":(519,),
            "CurieTemperature":(160,),
            "GammaCoefficient":(0.86,),
            "LongRangeInteractionLength":(1,),
            "InitPosition":(0,),
            "LongRangeExchangeFlag":False,
            "PeriodicBoundaryConditions":    False
            }

#"FeCr-FeCr" :2.72 - for TC=~162 K Ms=74.1
#"Fe-Fe"     :6 - for TC=~1070 K Ms=221.7

Hmin=0.0001
Hmax=1
Hsteps=32

Tmin=1
Tmax=300
Tsteps=64

from CalculationClass import simulation, timeit
from viewer import reader
# ctrl+shift+P: Debug Visualizer: New View

S=simulation(DeleteFlag=True,
             DescendingCoefficient=2,
             PathToFolder="debugFeCr",
             StructureParameters=FeCr_Parameters,
             StructureExchange=MaterialExchange,
             LongRangeExchange="none",
             NumberOfIterationM=50,
             NumberOfIterationTheta=1,
             NumberOfSteps=60)

S.mode(Debug=False)
S.GetMvsT(Tmin=Tmin,Tmax=Tmax,Tsteps=Tsteps,Hext=0.1)
S.ProcessMvsT(S.PathToFolderMT)
