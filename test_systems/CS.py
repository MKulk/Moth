FolderName          =   "CS_reuse"
Hmin,Hmax,Hsteps    =   -0.3,      0.1,      16
Tmin,Tmax,Tsteps    =   300,      300,    1
NumberOfSteps       =   24000
FieldDirection      =   0
Acceleration        =   1.0
DeleteFlag          =   False
ReusePreviousResults=   True
StructureParameters={
            "MaterialThickness":            (0.3,       6.0,        0.3,    ),
            "MLThickness":                  (0.15,      0.15,       0.15,   ),
            "ZeemanThickness":              (13.0,      1.0,        20.0,   ),
            "MaterialName":                 ("Py",      "FeCr",     "Py",   ),
            "MaterialS":                    (1,         1,          1,      ),
            "MaterialExtraField":           (0.2,       0,          0,      ),
            "MaterialExtraFieldDirection":  (0,         0,          0,      ),
            "MaterialSaturationM":          (800,       519,        800,    ),
            "CurieTemperature":             (0,         0,          0,      ),
            "GammaCoefficient":             (0.86,      0.86,       0.86,   ),
            "InitPosition":                 (90.0,      90.0,       90.0,   ),
            "InitB":                        (0.9,       0.74,       0.9,    ),
            "LongRangeInteractionLength":   (0.15,      1.0,        0.15,   ),
            "LongRangeExchangeFlag":         True,
            "InitPositionSingle":            10,
            "PeriodicBoundaryConditions":    False
            }
MaterialExchange={
            "Py-Py"     :0.23,
            "Py-FeCr"   :0.076,
            "FeCr-Py"   :0.076,
            "FeCr-FeCr" :0.023
            }

LongRangeExchange={
            "Py-FeCr"  :0.00015,
            "FeCr-Py"  :0.00015
            }#not used here
