import numpy as np
import os
from termcolor import colored
import math




class multilayer:
    def __init__(self,MaterialParameters,MaterialExchange,LongRangeExchange="none",Temperature=1,Field=1,FieldDirection=0):
        self.MaterialTotalThickness=np.sum(np.array(MaterialParameters["MaterialThickness"]))
        self.ExchangeTable                      =   MaterialExchange
        self.PeriodicBoundaryConditions         =   MaterialParameters["PeriodicBoundaryConditions"]
        self.NumberOfLayersConstruct            =   np.array(np.rint(np.array(MaterialParameters["MaterialThickness"])/np.array(MaterialParameters["MLThickness"])))
        self.MaterialName                       =   self.LayerConstructor(np.array(MaterialParameters["MaterialName"]))
        self.LayerNumber                        =   self.LayerConstructor(np.arange(len(MaterialParameters["MaterialName"])))
        self.MaterialS                          =   self.LayerConstructor(MaterialParameters["MaterialS"])
        self.MaterialExtraField                 =   self.LayerConstructor(MaterialParameters["MaterialExtraField"])
        self.MaterialExtraFieldDirection        =   self.LayerConstructor(MaterialParameters["MaterialExtraFieldDirection"])
        self.MaterialSaturationM                =   self.LayerConstructor(MaterialParameters["MaterialSaturationM"])
        self.CurieTemperature                   =   self.LayerConstructor(MaterialParameters["CurieTemperature"])
        self.MLThickness                        =   self.LayerConstructor(MaterialParameters["MLThickness"])
        self.space                              =   np.cumsum(self.MLThickness)
        self.GammaCoeff                         =   self.LayerConstructor(MaterialParameters["GammaCoefficient"])
        self.InitPosition                       =   self.LayerConstructor(MaterialParameters["InitPosition"])
        self.InitB                              =   self.LayerConstructor(MaterialParameters["InitB"])  
        self.LongRangeInteractionLength         =   self.LayerConstructor(MaterialParameters["LongRangeInteractionLength"])
        self.InitPositionSingle=   MaterialParameters["InitPositionSingle"]
        LongRangeExchangeFlag=MaterialParameters["LongRangeExchangeFlag"]
        if not LongRangeExchangeFlag:
            self.LongRangeExchangeFlag=False
            self.LongRangeExchange       =   np.zeros_like(self.MaterialSaturationM)
        else:
            self.LongRangeExchangeFlag=True
            self.LongRangeExchangeTable                  =   LongRangeExchange
        print("Long range exchange is in the state:"+str(self.LongRangeExchangeFlag))
        self.DefineExchange()
        #constants
        self.r                              =   self.TranslateConstant(1.3434) #g*ub/kb
        self.EMUtoJoulPerTesla              =   self.TranslateConstant(0.001)
        #external parameters
        self.Temperature                    =   self.TranslateConstant(Temperature)
        if Field<0:
            self.Field                          =   -Field
            self.FieldDirection                 =   180+FieldDirection
        else:
            self.Field                          =   Field
            self.FieldDirection                 =   FieldDirection
        self.pid=os.getpid()

    def SetExternalParameters(self, Field=0,FieldDirection=0,Temperature=1):
        if Field<0:
            self.Field                          =   -Field
            self.FieldDirection                 =   180+FieldDirection
        else:
            self.Field                          =   Field
            self.FieldDirection                 =   FieldDirection
        self.Temperature = Temperature

    def InitCalculation(self,NumberOfIterationM=5,NumberOfIterationTheta=100,NumberOfSteps=500,DescendingCoefficient=4):
        self.B          =   np.copy(self.InitB)#self.TranslateConstant(1)
        self.CHI        =   np.copy(self.InitB)#self.TranslateConstant(0.75)
        #self.ThetaM     =   self.TranslateConstant(self.InitPositionSingle)#360*(0.5-np.random.rand(self.B.size))#
        self.ThetaM     =   np.copy(self.InitPosition)
        self.NumberOfIterationM = NumberOfIterationM
        self.NumberOfIterationTheta = NumberOfIterationTheta
        self.NumberOfSteps = NumberOfSteps
        self.DescendingCoefficient = DescendingCoefficient
        self.Heffmax=self.Field+self.MaterialExtraField+self.MaterialSaturationM*self.Gamma+np.roll(self.MaterialSaturationM,-1)*self.GammaP1+np.roll(self.MaterialSaturationM,1)*self.GammaM1+np.roll(self.MaterialSaturationM,-2)*self.GammaP2+np.roll(self.MaterialSaturationM,2)*self.GammaM2
        self.Heff       =   self.TranslateConstant(0)
        self.delta=np.ones(self.B.size)*self.DescendingCoefficient
        #sliding masks preparation
        pattern1=np.array([True, False,False])
        pattern2=np.array([False,True ,False])
        pattern3=np.array([False,False,True])
        N=1+round(self.ThetaM.size/pattern1.size)
        repeat1=np.tile(pattern1,N)
        repeat2=np.tile(pattern2,N)
        repeat3=np.tile(pattern3,N)
        mask1=repeat1[0:self.ThetaM.size]
        mask2=repeat2[0:self.ThetaM.size]
        mask3=repeat3[0:self.ThetaM.size]
        #self.MaskSet=[mask1,mask2,mask3,mask3,mask2,mask1]
        self.MaskSet=[mask1,mask2,mask3,mask1,mask2,mask3]
        #biased element mask preparation
        self.Mip1            =   np.roll(np.arange(self.B.size),-1)
        self.Mim1            =   np.roll(np.arange(self.B.size),1)
        self.Mip2            =   np.roll(np.arange(self.B.size),-2)
        self.Mim2            =   np.roll(np.arange(self.B.size),2)
        if self.LongRangeExchangeFlag:
            self.CreateLongRangeMatrix()
        self.CalculateM()
        self.UpdateHeff()
        self.IterateMagnetisation()    
    
    def CreateLongRangeMatrix(self):
        """This function creates the 2d matrix that describes which element interact with which neighbour with which coefficient"""
        def flip(a):
            #flip 2d array along main diagonal
            b=np.zeros_like(a)
            for i in range(a[0].size):
                for j in range(a[0].size):
                    b[j,i] = a[i,j]
            return b
        patternP=np.zeros(self.MaterialName.size,dtype=float)
        patternM=np.zeros(self.MaterialName.size,dtype=float)
        index=-1
        delta=0
        name1=self.MaterialName[-1]
        #create exponential profiles for left-to-right and right-to-left 
        for i in range(self.MaterialName.size):
            if index-self.LayerNumber[i]==-1:
                exchangeName=name1+"-"+self.MaterialName[i]
                if exchangeName in self.LongRangeExchangeTable:
                    gammaLongRange=self.LongRangeExchangeTable[exchangeName]
                else:
                    gammaLongRange=0
                z=-delta*self.MLThickness[i]
                val=math.e**(z/self.LongRangeInteractionLength[i])
                if abs(val)>0.01:
                    patternP[i]=gammaLongRange*val
                delta+=1
            else:
                name1=self.MaterialName[i-1]
                delta=0
                z=-delta*self.MLThickness[i]
                val=math.e**(z/self.LongRangeInteractionLength[i])
                if abs(val)>0.01:
                    patternP[i]=gammaLongRange*val
                delta+=1
                index+=1
        index=self.LayerNumber[-1]+1
        delta=0
        for i in reversed(range(self.MaterialName.size)):
            if index-self.LayerNumber[i]==1:
                z=delta*self.MLThickness[i]
                val=math.e**(z/self.LongRangeInteractionLength[i])
                if abs(val)>0.01:
                    patternM[i]=val
                delta-=1
            else:
                delta=0
                z=delta*self.MLThickness[i]
                val=math.e**(z/self.LongRangeInteractionLength[i])
                if abs(val)>0.01:
                    patternM[i]=val
                delta-=1
                index-=1
        #create matrix of exponents
        MatrixP=np.zeros((patternP.size,patternP.size))
        MatrixM=np.zeros((patternM.size,patternM.size))


        for i in range(self.MaterialName.size):
            CurrentMonoLayerNumber=self.LayerNumber[i]
            maskR=self.LayerNumber==CurrentMonoLayerNumber+1
            maskL=self.LayerNumber==CurrentMonoLayerNumber-1
            MatrixP[i,maskR]=patternP[maskR]
            MatrixM[maskL,i]=patternM[maskL]
        NeighboursWeightP=MatrixM*MatrixP
        NeighboursWeightM=flip(NeighboursWeightP)
        NeighboursWeight=NeighboursWeightP+NeighboursWeightM
        #NeighboursWeight[NeighboursWeight<0.05]=0
        self.NeighboursWeight=NeighboursWeight
        self.NeighboursWeightMask=NeighboursWeight!=0
        self.NeighboursWeightZero=np.zeros(self.B.size,dtype=bool)
        for i in range(self.B.size):
            self.NeighboursWeightZero[i]=np.any(self.NeighboursWeightMask[i])
        
        #for i in range(self.B.size):
        #    for j in range(self.B.size):
        #        print(i, j, self.NeighboursWeight[i,j])
        return 0

    def CalculateM(self):
        self.M=self.MaterialSaturationM*self.B
        return 0
    def UpdateHexi(self):
        #effective field calculaion. Not sure about the volume normalization
        self.Hexi       =   self.Dot(self.M,1,0,self.Gamma)#self exchange
        return 0
    def UpdateHexN(self):
        #calculate direct exchange
        Hex1            =   (self.Dot(self.M[self.Mim1],1,self.ThetaM[self.Mim1]-self.ThetaM,self.GammaM1)+self.Dot(self.M[self.Mip1],1,self.ThetaM[self.Mip1]-self.ThetaM,self.GammaP1))
        Hex2            =   (self.Dot(self.M[self.Mim2],1,self.ThetaM[self.Mim2]-self.ThetaM,self.GammaM2)+self.Dot(self.M[self.Mip2],1,self.ThetaM[self.Mip2]-self.ThetaM,self.GammaP2))
        self.HexN       =   Hex1+Hex2
        if self.LongRangeExchangeFlag:
            LongRangeExchangeEnergy=np.zeros_like(self.M)
            for i in range(self.M.size):
                if not self.NeighboursWeightZero[i]:
                    LongRangeExchangeEnergy[i]=0
                else:
                    LongRangeExchangeEnergy[i]=np.sum(self.Dot(self.M[self.NeighboursWeightMask[i]],1,self.ThetaM[self.NeighboursWeightMask[i]]-self.ThetaM[i],self.NeighboursWeight[i,self.NeighboursWeightMask[i]]))
            self.LongRangeExchange       =   LongRangeExchangeEnergy #actually field but who cares
        return 0

    def UpdateHzz(self):
        #Zeeman with external field + Zeeman with supplementary field
        self.Hezz       =   self.Dot(self.Field,1,self.ThetaM-self.FieldDirection,1)+self.Dot(self.MaterialExtraField,1,self.ThetaM-self.MaterialExtraFieldDirection,1)
        return 0
    def UpdateHeff(self):
        self.UpdateHexi()
        self.UpdateHexN()
        self.UpdateHzz()
        self.Heff=self.Hezz+self.Hexi+self.HexN+self.LongRangeExchange
    def IterateMagnetisation(self,Number=0):
        if Number==0:
            Number=self.NumberOfIterationM
        for i in range(Number):
            self.UpdateHeff()
            self.Brillouin()
            self.CalculateCHI()
            self.CalculateM()
        self.UpdateHeff()
    def IterateSystem(self):
        self.delta=np.ones_like(self.ThetaM)*self.DescendingCoefficient
        self.delta=self.DescendingCoefficient
        self.IterateMagnetisation(Number=250)
        Told=np.copy(self.ThetaM)
        Bold=np.copy(self.B)
        printFlag=True
        for i in range(self.NumberOfSteps):
            self.MinimizeOrientation()
            self.IterateMagnetisation()
            dtheta=self.ThetaM-Told
            dB=self.B-Bold
            Told=np.copy(self.ThetaM)
            Bold=np.copy(self.B)
            
            BError=1e-2
            #TError=1e-5
            Bprecision=1e-7
            Tprecision=1e-4
            #if i>62:
            #    for s in range(self.B.size):
            #        print(i, s, self.B[s])
            #cheatMask=np.abs(self.B)>BError
            #if i>20 and np.any(np.abs(dtheta)>Tprecision):
            #    cheatMaskM=np.abs(self.B)>BError
            #    cheatMaskT=np.abs(dtheta)>Tprecision
            #    cheatMask=np.logical_and(cheatMaskM,cheatMaskT)
            #    #blockMask=np.abs(dtheta)<0.2
            #    #cheatMask=np.logical_and(cheatMask,blockMask)
            #    k=0.0  # 0.87 is maximum stable acceleration, the bigger number may destabilize the solutiuon
            #    self.ThetaM[cheatMask]=self.ThetaM[cheatMask]+k*dtheta[cheatMask] 
            if i>10 and np.all(np.abs(dtheta)<Tprecision) and np.all(np.abs(dB)<Bprecision):
                s1="Exit by precision for: "
                s2="T="+str(self.Temperature)
                s3=" H="+str(self.Field)
                s4=" after "+str(i)+" iterations"
                print(colored(s1, 'blue'), colored(s2, 'red'),colored(s3, 'red'),colored(s4,'blue'))
                printFlag=False
                break
            #nn=28
            #print(i, self.ThetaM[nn],self.M[nn])
        self.NormalizeThetaM()
        self.IterateMagnetisation(Number=250)
        if printFlag:
            s1="Exit by number of iterations for: "
            s2="T="+str(self.Temperature)
            s3=" H="+str(self.Field)
            print(colored(s1, 'blue'), colored(s2, 'red'),colored(s3, 'red'))
        


    def MinimizeOrientation(self):
        for i in range(2):
            for M in self.MaskSet:
                """the optimal position is max projection of HexN+Hzz"""
                self.UpdateHeff()
                Heff=self.HexN+self.Hezz+self.LongRangeExchange
                OldTheta=np.copy(self.ThetaM)
                self.ThetaM[M]=OldTheta[M]+self.delta #plus deviation
                self.UpdateHexN()
                self.UpdateHzz()
                Heffp=self.HexN+self.Hezz+self.LongRangeExchange
                self.ThetaM[M]=OldTheta[M]-self.delta #minus deviation
                self.UpdateHexN()
                self.UpdateHzz()
                Heffm=self.HexN+self.Hezz+self.LongRangeExchange
                self.ThetaM[M]=OldTheta[M]
                #check condition of minimum
                C1=np.logical_and((Heff<Heffp),(Heff<Heffm))
                TC1p=Heffp>Heffm #do not stay in the middle
                TC1m=np.logical_not(TC1p)
                shift1=self.delta*TC1p-self.delta*TC1m
                #check condition of slope
                s1=np.logical_and(Heffm<Heff,Heff<Heffp)
                s2=np.logical_and(Heffp<Heff,Heff<Heffm)
                C2=np.logical_or(s1,s2)
                TC2p=Heffp>Heffm
                TC2m=np.logical_not(TC2p)
                shift2=self.delta*TC2p-self.delta*TC2m
                #check the condition of near max
                C3=np.logical_and((Heff>Heffp),(Heff>Heffm))
                C3=np.logical_and(C3,Heffp!=Heffm)
                Sp=(Heffp-Heff)/self.delta
                Sm=(Heff-Heffm)/self.delta
                dSpm=Sp-Sm
                dSpm[dSpm==0]=1.0#1e-20
                shift3=(-Sm*self.delta/dSpm)-self.delta/2
                #calculate total shift
                shift=np.zeros_like(self.ThetaM)
                shift[C1]=shift1[C1]
                shift[C2]=shift2[C2]
                shift[C3]=shift3[C3]
                self.ThetaM[M]=self.ThetaM[M]+1.5*shift[M]
                self.IterateMagnetisation()#not lower than 40!!!!11111
        self.NormalizeThetaM()

    def NormalizeThetaM(self):
        k=self.ThetaM/180
        maskP=k>1
        maskM=k<-1
        prop=np.abs(np.rint(k/2))
        self.ThetaM[maskP]=self.ThetaM[maskP]-prop[maskP]*360
        self.ThetaM[maskM]=self.ThetaM[maskM]+prop[maskM]*360
        return 0

    def CalculateCHI(self):
        J=self.MaterialS
        r=self.r
        T=self.Temperature
        #self.CHI=(r*J*self.Heff/T)+(3*Tc*J/(T*(J+1)))*self.B
        J=self.MaterialS
        self.CHI=r*J*self.Heff/T 
        return 0 

    def Brillouin(self):
        S=self.MaterialS
        self.B=((2*S+1)/(2*S))*self.coth(self.CHI*((2*S+1)/(2*S)))-(1/(2*S))*self.coth(self.CHI/(2*S))
        #self.B=np.abs(self.B)
        return 0 

    def LayerConstructor(self,pattern):
        pattern=np.array(pattern)
        N=np.array(self.NumberOfLayersConstruct)
        result=np.empty(shape=0,dtype=pattern.dtype)
        for i in range(N.size):
            arr=np.full(int(N[i]),pattern[i])
            result=np.append(result,arr)
        return result

    def TranslateConstant(self,const):
        return np.full(self.MaterialName.shape,const,dtype=float)

    def DefineExchange(self):
        #define i-1 element
        tmp = np.roll(self.MaterialName,1)
        CombinationNamesM=np.core.defchararray.add(self.MaterialName, "-")
        CombinationNamesM=np.core.defchararray.add(CombinationNamesM, tmp)
        GammaM1 =np.zeros_like(self.MaterialName,dtype=float)
        #RKKYM1  =np.zeros_like(self.MaterialName,dtype=float)
        for i in range(GammaM1.size):
            GammaM1[i]=self.ExchangeTable[CombinationNamesM[i]]
            #if self.RKKYactive:
            #    if CombinationNamesM[i] in self.RKKYExchangeTable:
            #        RKKYM1[i]=self.RKKYExchangeTable[CombinationNamesM[i]]

        if not self.PeriodicBoundaryConditions:
            GammaM1[0]=0
            #RKKYM1[0]=0
        #define i-2 element
        tmp = np.roll(self.MaterialName,2)
        CombinationNamesM=np.core.defchararray.add(self.MaterialName, "-")
        CombinationNamesM=np.core.defchararray.add(CombinationNamesM, tmp)
        GammaM2=np.zeros_like(self.MaterialName,dtype=float)
        #RKKYM2  =np.zeros_like(self.MaterialName,dtype=float)
        for i in range(GammaM2.size):
            GammaM2[i]=self.ExchangeTable[CombinationNamesM[i]]
            #if self.RKKYactive:
            #    if CombinationNamesM[i] in self.RKKYExchangeTable:
            #        RKKYM2[i]=self.RKKYExchangeTable[CombinationNamesM[i]]
        if not self.PeriodicBoundaryConditions:
            GammaM2[0]=0
            GammaM2[1]=0
            #RKKYM2[0]=0
            #RKKYM2[1]=0
        #define i+1 element
        tmp = np.roll(self.MaterialName,-1)
        CombinationNamesP=np.core.defchararray.add(self.MaterialName, "-")
        CombinationNamesP=np.core.defchararray.add(CombinationNamesP, tmp)
        GammaP1=np.zeros_like(self.MaterialName,dtype=float)
        #RKKYP1  =np.zeros_like(self.MaterialName,dtype=float)
        for i in range(GammaP1.size):
            GammaP1[i]=self.ExchangeTable[CombinationNamesP[i]]
            #if self.RKKYactive:
            #    if CombinationNamesP[i] in self.RKKYExchangeTable:
            #        RKKYP1[i]=self.RKKYExchangeTable[CombinationNamesP[i]]
        if not self.PeriodicBoundaryConditions:
            GammaP1[-1]=0
            #RKKYP1[-1]=0
        #define i+2 element
        tmp = np.roll(self.MaterialName,-2)
        CombinationNamesP=np.core.defchararray.add(self.MaterialName, "-")
        CombinationNamesP=np.core.defchararray.add(CombinationNamesP, tmp)
        GammaP2=np.zeros_like(self.MaterialName,dtype=float)
        #RKKYP2  =np.zeros_like(self.MaterialName,dtype=float)
        for i in range(GammaP2.size):
            GammaP2[i]=self.ExchangeTable[CombinationNamesP[i]]
            #if self.RKKYactive:
            #    if CombinationNamesP[i] in self.RKKYExchangeTable:
            #        RKKYP2[i]=self.RKKYExchangeTable[CombinationNamesP[i]]
        if not self.PeriodicBoundaryConditions:
            GammaP2[-1]=0
            GammaP2[-2]=0
            #RKKYP2[-1]=0
            #RKKYP2[-2]=0
        #define i element
        CombinationNames=np.core.defchararray.add(self.MaterialName, "-")
        CombinationNames=np.core.defchararray.add(CombinationNames, self.MaterialName)
        Gamma=np.zeros_like(self.MaterialName,dtype=float)
        for i in range(Gamma.size):
            Gamma[i]=self.ExchangeTable[CombinationNames[i]]
        self.Gamma=Gamma*4
        self.GammaM1=4*GammaM1/self.GammaCoeff
        self.GammaM2=GammaM2*1
        self.GammaP1=4*GammaP1/self.GammaCoeff
        self.GammaP2=GammaP2*1
        #self.RKKYM1=4*RKKYM1/self.GammaCoeff
        #self.RKKYM2=RKKYM2*1
        #self.RKKYP1=4*RKKYP1/self.GammaCoeff
        #self.RKKYP2=RKKYP2*1
        return 0

    def coth(self,arg):
        s=np.tanh(arg)
        mask=s!=0.
        result=np.zeros_like(arg)
        result[mask]=1/s[mask]
        return result

    def Dot(self,A,B,Theta,const):
        return const*A*B*np.cos(np.radians(Theta))
