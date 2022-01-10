SAFParameters={
            "MaterialThickness":            (0.6,       1.2,        0.6,        ),
            "MLThickness":                  (0.15,      0.15,       0.15,       ),
            "MaterialName":                 ("Fe",      "FeCr",     "Fe",       ),
            "MaterialS":                    (1,         1,          1,          ),
            "MaterialExtraField":           (0,         0,          0,          ),
            "MaterialExtraFieldDirection":  (0,         0,          0,          ),
            "MaterialSaturationM":          (1500,      519,        1500,       ),
            "CurieTemperature":             (0,         0,          0,          ),
            "GammaCoefficient":             (0.86,      0.86,       0.86,       ),
            "InitPosition":                 (45.0,      0.0,       -45.0,       ),
            "InitB":                        (0.75,      0.74,       0.75,       ),
            "LongRangeInteractionLength":   (0.15,      0.45,       0.15,       ),
            "LongRangeExchangeFlag":         True,
            "InitPositionSingle":            10,
            "PeriodicBoundaryConditions":    False
            }
MaterialExchange={
            "FeCr-FeCr" :0.045,
            "Fe-FeCr"   :0.000,
            "FeCr-Fe"   :0.000,
            "Fe-Fe"     :0.09
            }
#Tc=300K gamma=0.045
RKKYExchange={
            "Fe-FeCr"  :-0.0018,
            "FeCr-Fe"  :-0.0018
            }



from CalculationClass import simulation, timeit
from viewer import reader

@timeit
def f(PathToFolder,StructureParameters,StructureExchange,LongRangeExchange):
    Hmin=0.001
    Hmax=1.0
    Hsteps=16
    Tmin=250
    Tmax=350
    Tsteps=16
    S=simulation(DeleteFlag=True,
                 DescendingCoefficient=2,
                 PathToFolder=PathToFolder,
                 StructureParameters=StructureParameters,
                 StructureExchange=StructureExchange,
                 LongRangeExchange=LongRangeExchange,
                 NumberOfIterationM=50,
                 NumberOfIterationTheta=1,
                 NumberOfSteps=1000)
    S.mode(Debug=False)
    file=S.GetMHvsT(
                    Hmin=Hmin,
                    Hmax=Hmax,
                    Hsteps=Hsteps,
                    Tmin=Tmin,
                    Tmax=Tmax,
                    Tsteps=Tsteps,
                    FieldDirection=0)
    data=reader(file)
    data.GetMHonT()
    data.GetMTonH()

#Long range exchange length=0.45
f(PathToFolder="F-f-F AF-RKKY H=0-1 T=250-350 16x16",StructureParameters=SAFParameters5,StructureExchange=MaterialExchange,LongRangeExchange=RKKYExchange)
