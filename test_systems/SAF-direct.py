
SAFParameters5={
            "MaterialThickness":            (1.2,       1.2,        1.2,        1.2,        1.2,        1.2,        1.2,        1.2,        1.2     ),
            "MLThickness":                  (0.15,      0.15,       0.15,       0.15,       0.15,       0.15,       0.15,       0.15,       0.15    ),
            "ZeemanThickness":              (1.0,       1.0,        1.0,        1.0,        1.0,        1.0,        1.0,        1.0,        1.0     ),
            "MaterialName":                 ("FeCr1",   "FeCr2",    "FeCr1",    "FeCr2",    "FeCr1",    "FeCr2",    "FeCr1",    "FeCr2",   "FeCr1"  ),
            "MaterialS":                    (1,         1,          1,          1,          1,          1,          1,          1,          1       ),
            "MaterialExtraField":           (0,         0,          0,          0,          0,          0,          0,          0,          0       ),
            "MaterialExtraFieldDirection":  (0,         0,          0,          0,          0,          0,          0,          0,          0       ),
            "MaterialSaturationM":          (778.5,     778.5,      778.5,      778.5,      778.5,      778.5,      778.5,      778.5,      778.5   ),
            "CurieTemperature":             (0,         0,          0,          0,          0,          0,          0,          0,          0       ),
            "GammaCoefficient":             (0.86,      0.86,       0.86,       0.86,       0.86,       0.86,       0.86,       0.86,       0.86    ),
            "InitPosition":                 (45.0,      -45.0,      45.0,       -45.0,      45.0,       -45.0,      45.0,       -45.0,      45.0    ),
            "InitB":                        (0.75,      0.74,       0.75,       0.74,       0.75,       0.74,       0.75,       0.74,       0.75    ),
            "LongRangeInteractionLength":   (0.45,      0.45,       0.45,       0.45,       0.45,       0.45,       0.45,       0.45,       0.45    ),
            "LongRangeExchangeFlag":         False,
            "InitPositionSingle":            10,
            "PeriodicBoundaryConditions":    False
            }
MaterialExchange={
            "FeCr1-FeCr1"   :0.029,
            "FeCr2-FeCr1"   :-0.00145,
            "FeCr1-FeCr2"   :-0.00145,
            "FeCr2-FeCr2"   :0.029
            }
#Tc=300K gamma=0.045
RKKYExchange={
            "FeCr2-FeCr1"  :-0.0018,
            "FeCr1-FeCr2"  :-0.0018
            }



from CalculationClass import simulation, timeit
from viewer import reader

@timeit
def f(PathToFolder,StructureParameters,StructureExchange,LongRangeExchange):
    Hmin=0.0#338
    Hmax=0.5#1338
    Hsteps=64
    Tmin=288 #10
    Tmax=291#400
    Tsteps=32
    S=simulation(DeleteFlag=True,
                 DescendingCoefficient=2,
                 PathToFolder=PathToFolder,
                 StructureParameters=StructureParameters,
                 StructureExchange=StructureExchange,
                 LongRangeExchange=LongRangeExchange,
                 NumberOfIterationM=50,
                 NumberOfIterationTheta=1,
                 NumberOfSteps=24000)
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
#no long range interaction
#f(PathToFolder="SAF RKKY J=-0.0000 l=0.00 T=280-310",StructureParameters=SAFParameters0,StructureExchange=MaterialExchange,LongRangeExchange=RKKYExchange)

#Long range exchange length=0.15
#f(PathToFolder="SAF RKKY J=-0.0018 l=0.15",StructureParameters=SAFParameters1,StructureExchange=MaterialExchange,LongRangeExchange=RKKYExchange)

#Long range exchange length=0.3
#f(PathToFolder="SAF RKKY J=-0.0018 l=0.30 1-1",StructureParameters=SAFParameters2,StructureExchange=MaterialExchange,LongRangeExchange=RKKYExchange)

#Long range exchange length=0.45
f(PathToFolder="SAF direct RKKY 18000 288-291 64x32",StructureParameters=SAFParameters5,StructureExchange=MaterialExchange,LongRangeExchange=RKKYExchange)

#Long range exchange length=0.6
#f(PathToFolder="SAF RKKY J=-0.0018 l=0.60",StructureParameters=SAFParameters4,StructureExchange=MaterialExchange,LongRangeExchange=RKKYExchange)
