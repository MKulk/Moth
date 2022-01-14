CSParameter={
            "MaterialThickness":            (0.3,       6.0,        0.3,    ),
            "MLThickness":                  (0.15,      0.15,       0.15,   ),
            "ZeemanThickness":              (13.0,      1.0,        20.0,   ),
            "MaterialName":                 ("Py",      "FeCr",     "Py",   ),
            "MaterialS":                    (1,         1,          1,      ),
            "MaterialExtraField":           (0.2,       0,          0,      ),
            "MaterialExtraFieldDirection":  (0,         0,          0,      ),
            "MaterialSaturationM":          (1557,      519,        1557,   ),
            "CurieTemperature":             (0,         0,          0,      ),
            "GammaCoefficient":             (0.86,      0.86,       0.86,   ),
            "InitPosition":                 (0.0,       0.0,       -45.0,   ),
            "InitB":                        (0.9,       0.74,       0.9,    ),
            "LongRangeInteractionLength":   (0.15,      2.0,        0.15,   ),
            "LongRangeExchangeFlag":         True,
            "InitPositionSingle":            10,
            "PeriodicBoundaryConditions":    False
            }
MultilayerParametersold={
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
            "Py-FeCr"   :0.076,
            "FeCr-Py"   :0.076,
            "FeCr-FeCr" :0.023
            }
LongRangeExchange={
            "Py-FeCr"  :0.0005,
            "FeCr-Py"  :0.0005
            }



from CalculationClass import simulation, timeit
from viewer import reader
# ctrl+shift+P: Debug Visualizer: New View

@timeit
def f(PathToFolder,StructureParameters,StructureExchange,LongRangeExchange):
    Hmin=-0.1#338
    Hmax=0.1#1338
    Hsteps=32
    Tmin=1#10
    Tmax=300#400
    Tsteps=3
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

f(PathToFolder="CS test NO long range",StructureParameters=CSParameter,StructureExchange=MaterialExchange,LongRangeExchange=LongRangeExchange)
