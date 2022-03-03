FolderName          =   "Fe40Cr60-type2-short-T=50-380-FC-FC--0.0016"
Hmin,Hmax,Hsteps    =   -1.0,      1.0,      96
Tmin,Tmax,Tsteps    =   50,      380,    33
NumberOfSteps       =   30000
FieldDirection      =   0
Acceleration        =   1.0
DeleteFlag          =   True
ReusePreviousResults=   False

#Fe40Cr60
StructureParameters={
            "MaterialThickness":            (0.3,       1.2,        1.2,        0.3,        1.2,        1.2,        0.3,        ),
            "MLThickness":                  (0.15,      0.15,       0.15,       0.15,       0.15,       0.15,       0.15,       ),
            "ZeemanThickness":              (4.0,       1.0,        1.0,        4.0,        1.0,        1.0,        4.0,        ),
            "MaterialName":                 ("Fe",      "FeCr1",    "FeCr2",    "Fe",       "FeCr1",    "FeCr2",    "Fe",       ),
            "MaterialS":                    (1,         1,          1,          1,          1,          1,          1,          ),
            "MaterialExtraField":           (0,         0,          0,          0,          0,          0,          0,          ),
            "MaterialExtraFieldDirection":  (0,         0,          0,          0,          0,          0,          0,          ),
            "MaterialSaturationM":          (1700.0,    680.0,      680.0,      1700.0,     680.0,      680.0,      1700.0,     ),
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
            "FeCr1-FeCr1"   :0.04,
            "FeCr1-FeCr2"   :-0.0016,#08
            "FeCr1-Fe"      :-0.001,
            "FeCr2-FeCr2"   :0.04,
            "FeCr2-FeCr1"   :-0.0016,#08
            "FeCr2-Fe"      :-0.001,
            "Fe-Fe"         :0.3,
            "Fe-FeCr1"      :-0.001,
            "Fe-FeCr2"      :-0.001
            }

LongRangeExchange={
            "FeCr1-FeCr2"  :-0.0001,
            "FeCr1-Fe"     :-0.025,
            "FeCr2-FeCr1"  :-0.0001,
            "FeCr2-Fe"     :-0.025,
            "Fe-FeCr1"     :-0.025,
            "Fe-FeCr2"     :-0.0225
            }#not used here
