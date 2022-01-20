FolderName          =   "test"
Hmin,Hmax,Hsteps    =   0,      1,      2
Tmin,Tmax,Tsteps    =   10,     300,    2
NumberOfSteps       =   24000
FieldDirection      =   0
StructureParameters={
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
            "LongRangeExchangeFlag":         False,
            "InitPositionSingle":            10,
            "PeriodicBoundaryConditions":    False
            }
MaterialExchange={
            "FeCr1-FeCr1"   :0.029,
            "FeCr1-FeCr2"   :-0.0014*3.5,
            "FeCr1-Fe"      :-0.002*3.5,
            "FeCr2-FeCr2"   :0.029,
            "FeCr2-FeCr1"   :-0.0014*3.5,
            "FeCr2-Fe"      :-0.002*3.5,
            "Fe-Fe"         :0.300,
            "Fe-FeCr1"      :-0.002*3.5,
            "Fe-FeCr2"      :-0.002*3.5
            }

LongRangeExchange={
            "FeCr1-FeCr2"  :-0.0014,
            "FeCr1-Fe"     :-0.002,
            "FeCr2-FeCr1"  :-0.0014,
            "FeCr2-Fe"     :-0.002,
            "Fe-FeCr1"     :-0.002,
            "Fe-FeCr2"     :-0.002
            }