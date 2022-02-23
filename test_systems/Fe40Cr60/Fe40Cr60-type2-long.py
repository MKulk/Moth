
SAFParameters5={
            "MaterialThickness":            (0.3,       1.2,        1.2,        0.3,        1.2,        1.2,        0.3,        ),
            "MLThickness":                  (0.15,      0.15,       0.15,       0.15,       0.15,       0.15,       0.15,       ),
            "ZeemanThickness":              (4.0,       1.0,        1.0,        4.0,        1.0,        1.0,        4.0,        ),
            "MaterialName":                 ("Fe",      "FeCr1",    "FeCr2",    "Fe",       "FeCr1",    "FeCr2",    "Fe",       ),
            "MaterialS":                    (1,         1,          1,          1,          1,          1,          1,          ),
            "MaterialExtraField":           (0,         0,          0,          0,          0,          0,          0,          ),
            "MaterialExtraFieldDirection":  (0,         0,          0,          0,          0,          0,          0,          ),
            "MaterialSaturationM":          (1557.0,    778.5,      778.5,      1557.0,     778.5,      778.5,      1557.0,     ),
            "CurieTemperature":             (0,         0,          0,          0,          0,          0,          0,          ),
            "GammaCoefficient":             (0.86,      0.86,       0.86,       0.86,       0.86,       0.86,       0.86,       ),
            "InitPosition":                 (80.0,      -80.0,      80.0,       -80.0,      80.0,       -80.0,      80.0,       ),
            "InitB":                        (0.75,      0.74,       0.74,       0.75,       0.74,       0.74,       0.75,       ),
            "LongRangeInteractionLength":   (0.15,      0.45,       0.45,       0.15,       0.45,       0.45,       0.15,       ),
            "LongRangeExchangeFlag":         True,
            "InitPositionSingle":            10,
            "PeriodicBoundaryConditions":    False
            }
MaterialExchange={
            "FeCr1-FeCr1"   :0.029,
            "FeCr1-FeCr2"   :0.000,
            "FeCr1-Fe"      :0.000,
            "FeCr2-FeCr2"   :0.029,
            "FeCr2-FeCr1"   :0.000,
            "FeCr2-Fe"      :0.000,
            "Fe-Fe"         :0.300,
            "Fe-FeCr1"      :0.000,
            "Fe-FeCr2"      :0.000
            }
#Tc=300K gamma=0.045
RKKYExchange={
            "FeCr1-FeCr2"  :-0.0014,
            "FeCr1-Fe"     :-0.002,
            "FeCr2-FeCr1"  :-0.0014,
            "FeCr2-Fe"     :-0.002,
            "Fe-FeCr1"     :-0.002,
            "Fe-FeCr2"     :-0.002
            }



from CalculationClass import simulation, timeit
from viewer import reader

@timeit
def f(PathToFolder,StructureParameters,StructureExchange,LongRangeExchange):
    Hmin=0.0#338
    Hmax=0.1#1338
    Hsteps=32
    Tmin=296 #10
    Tmax=316#400
    Tsteps=32
    S=simulation(DeleteFlag=True,
                 DescendingCoefficient=2,
                 PathToFolder=PathToFolder,
                 StructureParameters=StructureParameters,
                 StructureExchange=StructureExchange,
                 LongRangeExchange=LongRangeExchange,
                 NumberOfIterationM=50,
                 NumberOfIterationTheta=1,
                 NumberOfSteps=6000)
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
f(PathToFolder="1-3 SAF J_RKKY=5 proc l=0.45  6000 32x32 296-316",StructureParameters=SAFParameters5,StructureExchange=MaterialExchange,LongRangeExchange=RKKYExchange)

#Long range exchange length=0.6
#f(PathToFolder="SAF RKKY J=-0.0018 l=0.60",StructureParameters=SAFParameters4,StructureExchange=MaterialExchange,LongRangeExchange=RKKYExchange)
