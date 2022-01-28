FolderName          =   "SAF-0.45nm-5proc"
Hmin,Hmax,Hsteps    =   0.001,      0.5,      64
Tmin,Tmax,Tsteps    =   274,      314,    128
NumberOfSteps       =   24000
FieldDirection      =   0
Acceleration        =   1.0
StructureParameters={
            "MaterialThickness":            (1.2,       1.2,        1.2,        1.2,        1.2,        1.2,        1.2,        1.2,        1.2     ),
            "MLThickness":                  (0.15,      0.15,       0.15,       0.15,       0.15,       0.15,       0.15,       0.15,       0.15    ),
            "ZeemanThickness":              (1.0,       1.0,        1.0,        1.0,        1.0,        1.0,        1.0,        1.0,        1.0     ),
            "MaterialName":                 ("FeCr1",   "FeCr2",    "FeCr1",    "FeCr2",    "FeCr1",    "FeCr2",    "FeCr1",    "FeCr2",   "FeCr1"  ),
            "MaterialS":                    (1,         1,          1,          1,          1,          1,          1,          1,          1       ),
            "MaterialExtraField":           (0,         0,          0,          0,          0,          0,          0,          0,          0       ),
            "MaterialExtraFieldDirection":  (0,         0,          0,          0,          0,          0,          0,          0,          0       ),
            "MaterialSaturationM":          (519,       519,        519,        519,        519,        519,        519,        519,        519     ),
            "CurieTemperature":             (0,         0,          0,          0,          0,          0,          0,          0,          0       ),
            "GammaCoefficient":             (0.86,      0.86,       0.86,       0.86,       0.86,       0.86,       0.86,       0.86,       0.86    ),
            "InitPosition":                 (45.0,      -45.0,      45.0,       -45.0,      45.0,       -45.0,      45.0,       -45.0,      45.0    ),
            "InitB":                        (0.75,      0.74,       0.75,       0.74,       0.75,       0.74,       0.75,       0.74,       0.75    ),
            "LongRangeInteractionLength":   (0.45,      0.45,       0.45,       0.45,       0.45,       0.45,       0.45,       0.45,       0.45    ),
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

LongRangeExchange={
            "Py-FeCr"  :-0.00225,
            "FeCr-Py"  :-0.00225
            }
