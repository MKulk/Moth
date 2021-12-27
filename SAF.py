SAFParameters={
            "MaterialThickness":            (1.2,       1.2,        1.2,        1.2,        1.2,        1.2,        1.2,        1.2),
            "MLThickness":                  (0.15,      0.15,       0.15,       0.15,       0.15,       0.15,       0.15,       0.15),
            "MaterialName":                 ("FeCr1",   "FeCr2",    "FeCr1",    "FeCr2",    "FeCr1",    "FeCr2",    "FeCr1",    "FeCr2"),
            "MaterialS":                    (1,         1,          1,          1,          1,          1,          1,          1),
            "MaterialExtraField":           (0,         0,          0,          0,          0,          0,          0,          0),
            "MaterialExtraFieldDirection":  (0,         0,          0,          0,          0,          0,          0,          0),
            "MaterialSaturationM":          (519,       519,        519,        519,        519,        519,        519,        519),
            "CurieTemperature":             (0,         0,          0,          0,          0,          0,          0,          0),
            "GammaCoefficient":             (0.86,      0.86,       0.86,       0.86,       0.86,       0.86,       0.86,       0.86),
            "InitPosition":                 (80,        -80,        80,         -80,        80,         -80,        80,         -80),
            "LongRangeInteractionLength":   (0.15,      0.15,       0.15,       0.15,       0.15,       0.15,       0.15,       0.15),
            "LongRangeExchangeFlag":         True,
            "InitPositionSingle":            10,
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



from CalculationClass import simulation, timeit
from viewer import reader


def f(PathToFolder,StructureParameters,StructureExchange,LongRangeExchange):
    Hmin=0.001
    Hmax=1
    Hsteps=20
    Tmin=10
    Tmax=400
    Tsteps=32
    S=simulation(DeleteFlag=True,
                 DescendingCoefficient=2,
                 PathToFolder=PathToFolder,
                 StructureParameters=StructureParameters,
                 StructureExchange=StructureExchange,
                 LongRangeExchange=LongRangeExchange,
                 NumberOfIterationM=10,
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

#Long range exchange length=0.15
f(PathToFolder="SAF RKKY J=-0.0018 l=0.15",StructureParameters=SAFParameters,StructureExchange=MaterialExchange,LongRangeExchange=RKKYExchange)
#Long range exchange length=0.3
SAFParameters1=SAFParameters
SAFParameters1["LongRangeInteractionLength"]=SAFParameters["LongRangeInteractionLength"]*2
f(PathToFolder="SAF RKKY J=-0.0018 l=0.30",StructureParameters=SAFParameters1,StructureExchange=MaterialExchange,LongRangeExchange=RKKYExchange)
#Long range exchange length=0.45
SAFParameters2=SAFParameters
SAFParameters2["LongRangeInteractionLength"]=SAFParameters["LongRangeInteractionLength"]*3
f(PathToFolder="SAF RKKY J=-0.0018 l=0.45",StructureParameters=SAFParameters2,StructureExchange=MaterialExchange,LongRangeExchange=RKKYExchange)
