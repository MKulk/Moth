FolderName          =   "Fe40Cr60-3.0nm"
Hmin,Hmax,Hsteps    =   0.1,      0.1,      1
Tmin,Tmax,Tsteps    =   0,      450,    256
NumberOfSteps       =   2400
FieldDirection      =   0
Acceleration        =   1.5
DeleteFlag          =   True
ReusePreviousResults=   False

StructureParameters={
            "MaterialThickness":            (1.2,           ),
            "MLThickness":                  (0.15,          ),
            "ZeemanThickness":              (1.0,           ),
            "MaterialName":                 ("Fe40Cr60",    ),
            "MaterialS":                    (1,             ),
            "MaterialExtraField":           (0,             ),
            "MaterialExtraFieldDirection":  (0,             ),
            "MaterialSaturationM":          (680.0,         ),
            "CurieTemperature":             (0,             ),
            "GammaCoefficient":             (0.86,          ),
            "InitPosition":                 (0.0,           ),
            "InitB":                        (1.0,           ),
            "LongRangeInteractionLength":   (0.0,           ),
            "LongRangeExchangeFlag":         False,
            "InitPositionSingle":            0,
            "PeriodicBoundaryConditions":    False
            }
MaterialExchange={
            "Fe40Cr60-Fe40Cr60"   :0.04
            }

LongRangeExchange={
            "FeCr2-FeCr1"  :-0.0008,
            "FeCr1-FeCr2"  :-0.0008
            }#not used here