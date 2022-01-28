from Classes.CalculationClass import simulation
import numpy as np
Hmin,Hmax,Hsteps= -0.3, 0.1, 64
Tmin,Tmax,Tsteps    =100, 300, 32
S=simulation(DeleteFlag=False)
S.mode(Debug=True)
S.field=np.linspace(Hmin,Hmax,Hsteps)
S.Temperature=np.linspace(Tmin,Tmax,Tsteps)
S.GetPreviousResult(TargetFolder="CS_L=0.15nm_J=1proc",iH=12,iT=6,text="M(H)_profile")
