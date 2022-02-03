FolderName          =   "pinned_0"
Hmin,Hmax,Hsteps    =   -0.3,      0.1,      64
Tmin,Tmax,Tsteps    =   300,      300,    1
NumberOfSteps       =   24000
FieldDirection      =   0
Acceleration        =   1.0
DeleteFlag          =   False
StructureParameters={
            "MaterialThickness":            (0.3,       ),
            "MLThickness":                  (0.15,      ),
            "ZeemanThickness":              (13.0,      ),
            "MaterialName":                 ("Py",      ),
            "MaterialS":                    (1,         ),
            "MaterialExtraField":           (0.2,       ),
            "MaterialExtraFieldDirection":  (0,         ),
            "MaterialSaturationM":          (800,       ),
            "CurieTemperature":             (0,         ),
            "GammaCoefficient":             (0.86,      ),
            "InitPosition":                 (00.0,      ),
            "InitB":                        (0.9,       ),
            "LongRangeInteractionLength":   (0.15,      ),
            "LongRangeExchangeFlag":         False,
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
