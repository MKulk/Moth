FolderName          =   "Fe40Cr60-1.2nm-x8-long"
Hmin,Hmax,Hsteps    =   0.1,      0.1,      1
Tmin,Tmax,Tsteps    =   0,      450,    96
NumberOfSteps       =   24000
FieldDirection      =   0
Acceleration        =   1.5
DeleteFlag          =   True
ReusePreviousResults=   False

StructureParameters={
            "MaterialThickness":            (1.2,       1.2,        1.2,        1.2,        1.2,        1.2,        1.2,        1.2     ),
            "MLThickness":                  (0.15,      0.15,       0.15,       0.15,       0.15,       0.15,       0.15,       0.15    ),
            "ZeemanThickness":              (1.0,       1.0,        1.0,        1.0,        1.0,        1.0,        1.0,        1.0     ),
            "MaterialName":                 ("FeCr1",   "FeCr2",    "FeCr1",    "FeCr2",    "FeCr1",    "FeCr2",    "FeCr1",    "FeCr2" ),
            "MaterialS":                    (1,         1,          1,          1,          1,          1,          1,          1       ),
            "MaterialExtraField":           (0,         0,          0,          0,          0,          0,          0,          0       ),
            "MaterialExtraFieldDirection":  (0,         0,          0,          0,          0,          0,          0,          0       ),
            "MaterialSaturationM":          (680.0,     680.0,      680.0,      680.0,      680.0,      680.0,      680.0,      680.0   ),
            "CurieTemperature":             (0,         0,          0,          0,          0,          0,          0,          0       ),
            "GammaCoefficient":             (0.86,      0.86,       0.86,       0.86,       0.86,       0.86,       0.86,       0.86    ),
            "InitPosition":                 (45.0,      -45.0,      45.0,       -45.0,      45.0,       -45.0,      45.0,       -45.0   ),
            "InitB":                        (0.75,      0.74,       0.75,       0.74,       0.75,       0.74,       0.75,       0.74    ),
            "LongRangeInteractionLength":   (0.45,      0.45,       0.45,       0.45,       0.45,       0.45,       0.45,       0.45    ),
            "LongRangeExchangeFlag":         True,
            "InitPositionSingle":            10,
            "PeriodicBoundaryConditions":    False
            }
MaterialExchange={
            "FeCr1-FeCr1"   :0.04,
            "FeCr2-FeCr1"   :0.0,
            "FeCr1-FeCr2"   :0.0,
            "FeCr2-FeCr2"   :0.04
            }#when the long range exchange is activated dont forget to set corresponding material exchange to 0

LongRangeExchange={
            "FeCr2-FeCr1"  :-0.0001,#0,25%
            "FeCr1-FeCr2"  :-0.0001 #0,25%
            }#not used here
