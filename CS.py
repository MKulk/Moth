MultilayerParameters={
            "MaterialThickness":                (4,         6,          6   ),
            "MLThickness":                      (0.15,      0.15,       0.15),
            "MaterialName":                     ("Py",      "FeCr",     "Py"),
            "MaterialS":                        (1,         1,          1   ),
            "MaterialExtraField":               (0.2,       0,          0   ),
            "MaterialExtraFieldDirection":      (0,         0,          0   ),
            "MaterialSaturationM":              (800,       519,        800 ),
            "CurieTemperature":                 (1050,      160,        1050),
            "GammaCoefficient":                 (0.86,      0.86,       0.86),
            "InitPosition":                     (80,        80,         80   ),
            "LongRangeInteractionLength":       (0.15,       1,          0.15 ),
            "LongRangeExchangeFlag":            True,
            "PeriodicBoundaryConditions":       False,
            "InitPositionSingle":               0.0,
            "InitB":                            (0.75,      0.75,       0.75),
            }
MaterialExchange={
            "Py-Py"     :0.23,
            "Py-FeCr"   :0.23,
            "FeCr-Py"   :0.23,
            "FeCr-FeCr" :0.023
            }
LongRangeExchange={
            "Py-FeCr"  :0.0005,
            "FeCr-Py"  :0.0005
            }

Hmin=-0.07#5
Hmax=0.01
Hsteps=32

Tmin=1
Tmax=300
Tsteps=32

from CalculationClass import simulation, timeit
from viewer import reader
# ctrl+shift+P: Debug Visualizer: New View
@timeit
@timeit
def f(PathToFolder,StructureParameters,StructureExchange,LongRangeExchange):
    Hmin=-0.1#338
    Hmax=0.05#1338
    Hsteps=32
    Tmin=1#10
    Tmax=300#400
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

f(PathToFolder="saf test long range",StructureParameters=MultilayerParameters,StructureExchange=MaterialExchange,LongRangeExchange=LongRangeExchange)
