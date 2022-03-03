FolderName          =   "Fe40Cr60-type3-short-FM-AF"
Hmin,Hmax,Hsteps    =   0.0001,     1.0,      48
Tmin,Tmax,Tsteps    =   1,      400,    32
NumberOfSteps       =   96000
FieldDirection      =   0
Acceleration        =   1.0
DeleteFlag          =   True
ReusePreviousResults=   False


StructureParameters={
            "MaterialThickness":            (0.3,     2.4,        0.3,        2.4,        0.3,      2.4,        0.3,        2.4,       0.3,  ),
            "MLThickness":                  (0.15,    0.15,       0.15,       0.15,       0.15,     0.15,       0.15,       0.15,      0.15, ),
            "ZeemanThickness":              (8.0,     1.0,        8.0,        1.0,        8.0,      1.0,        8.0,        1.0,       8.0,  ),
            "MaterialName":                 ("Fe1",   "FeCr",     "Fe2",      "FeCr",     "Fe1",    "FeCr",     "Fe2",      "FeCr",    "Fe1",),
            "MaterialS":                    (1,       1,          1,          1,          1,        1,          1,          1,         1,    ),
            "MaterialExtraField":           (0,       0,          0,          0,          0,        0,          0,          0,         0,    ),
            "MaterialExtraFieldDirection":  (0,       0,          0,          0,          0,        0,          0,          0,         0,    ),
            "MaterialSaturationM":          (1700,    680,        1700,       680,        1700,     680,        1700,       680,       1700, ),
            "CurieTemperature":             (0,       0,          0,          0,          0,        0,          0,          0,         0,    ),
            "GammaCoefficient":             (0.86,    0.86,       0.86,       0.86,       0.86,     0.86,       0.86,       0.86,      0.86, ),
            "InitPosition":                 (45.0,    0.0,       -45.0,       0.0,        45.0,     0.0,        45.0,       0.0,       45.0, ),
            "InitB":                        (0.9,     0.74,       0.9,        0.74,       0.9,      0.74,       0.9,        0.74,      0.9,  ),
            "LongRangeInteractionLength":   (0.15,    0.45,       0.15,       0.45,       0.15,     0.45,       0.15,       0.45,      0.15, ),
            "LongRangeExchangeFlag":         False,
            "InitPositionSingle":            10,
            "PeriodicBoundaryConditions":    False
            }
MaterialExchange={
            "FeCr-FeCr" :0.04,
            "FeCr-Fe1"  :-0.0008,#AFM
            "FeCr-Fe2"  :0.0008, #FM
            "Fe1-Fe1"   :0.3,
            "Fe1-FeCr"  :-0.0008,
            "Fe1-Fe2"   :0.000,
            "Fe2-Fe2"   :0.3,
            "Fe2-FeCr"  :0.0008,
            "Fe2-Fe1"   :0.000
            }

LongRangeExchange={
            "Fe1-FeCr"  :-0.0006,
            "FeCr-Fe1"  :-0.0006,
            "Fe2-FeCr"  :0.0006,
            "FeCr-Fe2"  :0.0006
            }
