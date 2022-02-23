FolderName          =   "Fe50Cr50-1.2nm"
Hmin,Hmax,Hsteps    =   0.001,      0.5,      64
Tmin,Tmax,Tsteps    =   284,      291,    32
NumberOfSteps       =   10000
FieldDirection      =   0
StructureParameters={
            "MaterialThickness":            (1.2,       1.2,        1.2,        1.2,        1.2,        1.2,        1.2,        1.2     ),
            "MLThickness":                  (0.15,      0.15,       0.15,       0.15,       0.15,       0.15,       0.15,       0.15    ),
            "ZeemanThickness":              (1.0,       1.0,        1.0,        1.0,        1.0,        1.0,        1.0,        1.0     ),
            "MaterialName":                 ("FeCr1",   "FeCr2",    "FeCr1",    "FeCr2",    "FeCr1",    "FeCr2",    "FeCr1",    "FeCr2" ),
            "MaterialS":                    (1,         1,          1,          1,          1,          1,          1,          1       ),
            "MaterialExtraField":           (0,         0,          0,          0,          0,          0,          0,          0       ),
            "MaterialExtraFieldDirection":  (0,         0,          0,          0,          0,          0,          0,          0       ),
            "MaterialSaturationM":          (778.5,     778.5,      778.5,      778.5,      778.5,      778.5,      778.5,      778.5   ),
            "CurieTemperature":             (0,         0,          0,          0,          0,          0,          0,          0       ),
            "GammaCoefficient":             (0.86,      0.86,       0.86,       0.86,       0.86,       0.86,       0.86,       0.86    ),
            "InitPosition":                 (45.0,      -45.0,      45.0,       -45.0,      45.0,       -45.0,      45.0,       -45.0   ),
            "InitB":                        (0.75,      0.74,       0.75,       0.74,       0.75,       0.74,       0.75,       0.74    ),
            "LongRangeInteractionLength":   (0.45,      0.45,       0.45,       0.45,       0.45,       0.45,       0.45,       0.45    ),
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

LongRangeExchange={
            "FeCr2-FeCr1"  :-0.0018,
            "FeCr1-FeCr2"  :-0.0018
            }#not used here
