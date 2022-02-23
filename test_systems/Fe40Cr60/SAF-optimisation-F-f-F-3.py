FolderName          =   "SAF-optimization-F-f-FF-f-F-3"
Hmin,Hmax,Hsteps    =   0,      1.0,      32
Tmin,Tmax,Tsteps    =   290,      310,    15
NumberOfSteps       =   24000
FieldDirection      =   0
Acceleration        =   1.5
DeleteFlag          =   True
ReusePreviousResults=   False
StructureParameters={
            "MaterialThickness":            (0.60,    1.2,        1.2,        1.2,        0.60,   ),
            "MLThickness":                  (0.15,    0.15,       0.15,       0.15,       0.15,   ),
            "ZeemanThickness":              (1.0,     1.0,        1.0,        1.0,        1.0,    ),
            "MaterialName":                 ("Fe1",   "FeCr",     "Fe2",      "FeCr",     "Fe1",  ),
            "MaterialS":                    (1,       1,          1,          1,          1,      ),
            "MaterialExtraField":           (0,       0,          0,          0,          0,      ),
            "MaterialExtraFieldDirection":  (0,       0,          0,          0,          0,      ),
            "MaterialSaturationM":          (1500,    519,        1500,       519,        1500,   ),
            "CurieTemperature":             (0,       0,          0,          0,          0,      ),
            "GammaCoefficient":             (0.86,    0.86,       0.86,       0.86,       0.86,   ),
            "InitPosition":                 (45.0,    0.0,       -45.0,       0.0,        45.0,   ),
            "InitB":                        (0.9,     0.74,       0.9,        0.74,       0.9,    ),
            "LongRangeInteractionLength":   (0.15,    0.45,       0.15,       0.45,       0.15,   ),
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

LongRangeExchange={
            "Fe1-FeCr"  :-0.0006,
            "FeCr-Fe1"  :-0.0006,
            "Fe2-FeCr"  :0.0006,
            "FeCr-Fe2"  :0.0006
            }
