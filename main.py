MultilayerParameters={
            "MaterialThickness":(4,6,6),
            "MLThickness":(0.15,0.15,0.15),
            "MaterialName":("Py","FeCr","Py"),
            "MaterialS":(1,1,1),
            "MaterialExtraField":(0.2,0,0),
            "MaterialExtraFieldDirection":(0,0,0),
            "MaterialSaturationM":(800,519,800),
            "CurieTemperature":(1050,160,1050),
            "GammaCoefficient":(0.86,0.86,0.86)
            }
MaterialExchange={
            "Py-Py"     :0.051,
            "Py-FeCr"   :0.03,
            "FeCr-Py"   :0.03,
            "FeCr-FeCr" :0.0216
            }

Py_Parameters={
            "MaterialThickness":(50,),
            "MLThickness":(0.15,),
            "MaterialName":("Py",),
            "MaterialS":(1,),
            "MaterialExtraField":(0,),
            "MaterialExtraFieldDirection":(0,),
            "MaterialSaturationM":(800,),
            "CurieTemperature":(1050,),
            "GammaCoefficient":(0.78,)
            }
FeCr_Parameters={
            "MaterialThickness":(50,),
            "MLThickness":(0.15,),
            "MaterialName":("FeCr",),
            "MaterialS":(1,),
            "MaterialExtraField":(0,),
            "MaterialExtraFieldDirection":(0,),
            "MaterialSaturationM":(519,),
            "CurieTemperature":(160,),
            "GammaCoefficient":(0.78,)
            }

#"FeCr-FeCr" :2.72 - for TC=~162 K Ms=74.1
#"Fe-Fe"     :6 - for TC=~1070 K Ms=221.7

Hmin=-0.05
Hmax=0.01
Hsteps=64

Tmin=1
Tmax=300
Tsteps=2

from CalculationClass import simulation, timeit
from viewer import reader
# ctrl+shift+P: Debug Visualizer: New View
@timeit
def f():
    S=simulation(DeleteFlag=True,
                DescendingCoefficient=2,
                PathToFolder="debug",
                StructureParameters=FeCr_Parameters,
                StructureExchange=MaterialExchange,
                NumberOfIterationM=50,
                NumberOfIterationTheta=1,
                NumberOfSteps=60)

    S.mode(Debug=False)
    #S.GetMvsH(Hmin=Hmin,Hmax=Hmax,Hsteps=Hsteps,Text=170,FieldDirection=0)
    #S.ProcessMvsH(S.PathToFolderMH)
    
    #file=S.GetMHvsT(
    #            Hmin=Hmin,
    #            Hmax=Hmax,
    #            Hsteps=Hsteps,
    #            Tmin=20,
    #            Tmax=120,
    #            Tsteps=2,
    #            FieldDirection=0)
    #data=reader(file)
    #data.GetMHonT()
    S.GetMvsT(Tmin=Tmin,Tmax=Tmax,Tsteps=Tsteps,Hext=0.1)
    S.ProcessMvsT(S.PathToFolderMT)


f()