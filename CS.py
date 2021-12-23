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
            "LongRangeInteractionLength":       (0.3,       1,          0.3 ),
            "LongRangeExchangeFlag":            False,
            "PeriodicBoundaryConditions":       False
            }
MaterialExchange={
            "Py-Py"     :0.23,
            "Py-FeCr"   :0.23,
            "FeCr-Py"   :0.23,
            "FeCr-FeCr" :0.023
            }
LongRangeExchange={
            "FeCr2-FeCr1"  :-0.0018,
            "FeCr1-FeCr2"  :-0.0018
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
def f():
    S=simulation(DeleteFlag=True,
                DescendingCoefficient=2,
                PathToFolder="CS short range interaction only test debug",
                StructureParameters=MultilayerParameters,
                StructureExchange=MaterialExchange,
                NumberOfIterationM=40,
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



f()