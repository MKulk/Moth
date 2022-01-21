FolderName          =   "Fe50Cr50-1.2nm"
Hmin,Hmax,Hsteps    =   0.1,      0.1,      1
Tmin,Tmax,Tsteps    =   0,      450,    256
NumberOfSteps       =   2400
FieldDirection      =   0
StructureParameters={
            "MaterialThickness":            (1.2,   ),
            "MLThickness":                  (0.15,  ),
            "ZeemanThickness":              (1.0,   ),
            "MaterialName":                 ("FeCr",),
            "MaterialS":                    (1,     ),
            "MaterialExtraField":           (0,     ),
            "MaterialExtraFieldDirection":  (0,     ),
            "MaterialSaturationM":          (778.5, ),
            "CurieTemperature":             (0,     ),
            "GammaCoefficient":             (0.86,  ),
            "InitPosition":                 (0.0,   ),
            "InitB":                        (1.0,   ),
            "LongRangeInteractionLength":   (0.0,   ),
            "LongRangeExchangeFlag":         False,
            "InitPositionSingle":            0,
            "PeriodicBoundaryConditions":    False
            }
MaterialExchange={
            "FeCr-FeCr"   :0.029
            }

LongRangeExchange={
            "FeCr2-FeCr1"  :-0.0008,
            "FeCr1-FeCr2"  :-0.0008
            }#not used here