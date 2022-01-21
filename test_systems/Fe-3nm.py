FolderName          =   "Fe-3nm"
Hmin,Hmax,Hsteps    =   0,      1,      2
Tmin,Tmax,Tsteps    =   0,     2500,    128
NumberOfSteps       =   24000
FieldDirection      =   0
StructureParameters={
            "MaterialThickness":            (0.3,   ),
            "MLThickness":                  (0.15,  ),
            "ZeemanThickness":              (1.0,   ),
            "MaterialName":                 ("Fe",  ),
            "MaterialS":                    (1,     ),
            "MaterialExtraField":           (0,     ),
            "MaterialExtraFieldDirection":  (0,     ),
            "MaterialSaturationM":          (1557,  ),
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
            "Fe-Fe"       :0.3
            }

LongRangeExchange={
            "FeCr2-FeCr1"  :-0.0008,
            "FeCr1-FeCr2"  :-0.0008
            }#not used here