FolderName          =   "SAF-opt-F-f-F-direct-2%"
Hmin,Hmax,Hsteps    =   0,      1,      32
Tmin,Tmax,Tsteps    =   290,      310,    15
NumberOfSteps       =   24000
FieldDirection      =   0
Acceleration        =   1.5
DeleteFlag          =   True
ReusePreviousResults=   False
StructureParameters={
            "MaterialThickness":            (0.3,     1.2,        0.3,       ),
            "MLThickness":                  (0.15,    0.15,       0.15,      ),
            "ZeemanThickness":              (4.0,     1.0,        4.0,       ),
            "MaterialName":                 ("Fe1",   "FeCr",     "Fe1",     ),
            "MaterialS":                    (1,       1,          1,         ),
            "MaterialExtraField":           (0,       0,          0,         ),
            "MaterialExtraFieldDirection":  (0,       0,          0,         ),
            "MaterialSaturationM":          (1500,    519,        1500,      ),
            "CurieTemperature":             (0,       0,          0,         ),
            "GammaCoefficient":             (0.86,    0.86,       0.86,      ),
            "InitPosition":                 (45.0,    0.0,       -45.0,      ),
            "InitB":                        (0.9,     0.74,       0.9,       ),
            "LongRangeInteractionLength":   (0.15,    0.45,       0.15,      ),
            "LongRangeExchangeFlag":         False,
            "InitPositionSingle":            10,
            "PeriodicBoundaryConditions":    False
            }
MaterialExchange={
            "FeCr-FeCr" :0.045,
            "FeCr-Fe1"  :0.0003114,#2%
            "Fe1-Fe1"   :0.09,
            "Fe1-FeCr"  :0.0003114
            }

LongRangeExchange={
            "Fe1-FeCr"  :-0.0006,
            "FeCr-Fe1"  :-0.0006
            }

