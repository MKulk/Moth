SAFParameters={
            "MaterialThickness":            (1.2,       1.2,        1.2,        1.2,        1.2,        1.2,        1.2,        1.2),
            "MLThickness":                  (0.15,      0.15,       0.15,       0.15,       0.15,       0.15,       0.15,       0.15),
            "MaterialName":                 ("FeCr1",   "FeCr2",    "FeCr1",    "FeCr2",    "FeCr1",    "FeCr2",    "FeCr1",    "FeCr2"),
            "MaterialS":                    (1,         1,          1,          1,          1,          1,          1,          1),
            "MaterialExtraField":           (0,         0,          0,          0,          0,          0,          0,          0),
            "MaterialExtraFieldDirection":  (0,         0,          0,          0,          0,          0,          0,          0),
            "MaterialSaturationM":          (519,       519,        519,        519,        519,        519,        519,        519),
            "CurieTemperature":             (0,         0,          0,          0,          0,          0,          0,          0),
            "GammaCoefficient":             (0.78,      0.78,       0.78,       0.78,       0.78,       0.78,       0.78,       0.78),
            "InitPosition":                 (80,        -80,        80,         -80,        80,         -80,        80,         -80),
            "LongRangeInteractionLength":   (0.2,       0.2,        0.8,        0.8,        0.2,        0.2,        0.05,       1.0),
            "PeriodicBoundaryConditions":    False
            }
SAFParameters1={
            "MaterialThickness":            (1.2,       1.2),
            "MLThickness":                  (0.15,      0.15),
            "MaterialName":                 ("FeCr1",   "FeCr2"),
            "MaterialS":                    (1,         1),
            "MaterialExtraField":           (0,         0),
            "MaterialExtraFieldDirection":  (0,         0),
            "MaterialSaturationM":          (519,       519),
            "CurieTemperature":             (0,         0),
            "GammaCoefficient":             (0.78,      0.78),
            "InitPosition":                 (80,        -80),
            "LongRangeInteractionLength":   (0.2,       0.4),
            "PeriodicBoundaryConditions":    False
            }
MaterialExchange={
            "FeCr1-FeCr1"   :0.045,
            "FeCr2-FeCr1"   :0.000,
            "FeCr1-FeCr2"   :0.000,
            "FeCr2-FeCr2"   :0.045
            }
#Tc=300K gamma=0.045
RKKYExchange={
            "FeCr2-FeCr1"  :-0.0018,
            "FeCr1-FeCr2"  :-0.0018
            }

Hmin=0.0001
Hmax=1
Hsteps=32

Tmin=10
Tmax=400
Tsteps=64

from CalculationClass import simulation, timeit
from viewer import reader


S=simulation(DeleteFlag=True,
             DescendingCoefficient=2,
             PathToFolder="SAF RKKY test",
             StructureParameters=SAFParameters,
             StructureExchange=MaterialExchange,
             LongRangeExchange=RKKYExchange,
             NumberOfIterationM=50,
             NumberOfIterationTheta=1,
             NumberOfSteps=600)

S.mode(Debug=True)
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
