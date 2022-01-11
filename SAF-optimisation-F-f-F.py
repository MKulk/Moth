SAFParameters={
            "MaterialThickness":            (0.15,      1.2,        0.15,       1.2,        0.15,   ),
            "MLThickness":                  (0.15,      0.15,       0.15,       0.15,       0.15,   ),
            "ZeemanThickness":              (4.0,       1.0,        8.0,        1.0,        4.0,    ),
            "MaterialName":                 ("Fe1",     "FeCr",     "Fe2",      "FeCr",     "Fe1",  ),
            "MaterialS":                    (1,         1,          1,          1,          1,      ),
            "MaterialExtraField":           (0,         0,          0,          0,          0,      ),
            "MaterialExtraFieldDirection":  (0,         0,          0,          0,          0,      ),
            "MaterialSaturationM":          (1500,      519,        1500,       519,        1500,   ),
            "CurieTemperature":             (0,         0,          0,          0,          0,      ),
            "GammaCoefficient":             (0.86,      0.86,       0.86,       0.86,       0.86,   ),
            "InitPosition":                 (45.0,      0.0,       -45.0,       0.0,        45.0,   ),
            "InitB":                        (1.0,       0.74,       1.0,        0.74,       1.0,    ),
            "LongRangeInteractionLength":   (0.15,      0.45,       0.15,       0.45,       0.15,   ),
            "LongRangeExchangeFlag":         True,
            "InitPositionSingle":            10,
            "PeriodicBoundaryConditions":    False
            }
MaterialExchange={
            "FeCr-FeCr" :0.045,
            "FeCr-Fe1"  :0.000,
            "FeCr-Fe2"  :0.000,
            "Fe1-Fe1"   :0.09,
            "Fe1-FeCr"  :0.000,
            "Fe1-Fe2"   :0.000,
            "Fe2-Fe2"   :0.09,
            "Fe2-FeCr"  :0.000,
            "Fe2-Fe1"   :0.000
            }
#Tc=300K gamma=0.045
RKKYExchange={
            "Fe1-FeCr"  :-0.0006,
            "FeCr-Fe1"  :-0.0006,
            "Fe2-FeCr"  :0.0006,
            "FeCr-Fe2"  :0.0006
            }



from CalculationClass import simulation, timeit
from viewer import reader

@timeit
def f(PathToFolder,StructureParameters,StructureExchange,LongRangeExchange):
    Hmin=0.001
    Hmax=0.5
    Hsteps=32
    Tmin=290
    Tmax=310
    Tsteps=32
    S=simulation(DeleteFlag=True,
                 DescendingCoefficient=2,
                 PathToFolder=PathToFolder,
                 StructureParameters=StructureParameters,
                 StructureExchange=StructureExchange,
                 LongRangeExchange=LongRangeExchange,
                 NumberOfIterationM=50,
                 NumberOfIterationTheta=1,
                 NumberOfSteps=1200)
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
f(PathToFolder="F-f-F AF-RKKY H=0-1 T=280-320 32x32",StructureParameters=SAFParameters,StructureExchange=MaterialExchange,LongRangeExchange=RKKYExchange)
