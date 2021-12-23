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
        self.LongRangeInteractionLength         =   self.LayerConstructor(MaterialParameters["LongRangeInteractionLength"])
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
        self.B          =   self.TranslateConstant(1)
        self.CHI        =   self.TranslateConstant(0.75)
        self.ThetaM     =   self.TranslateConstant(90)#360*(0.5-np.random.rand(self.B.size))#
        #self.ThetaM     =   self.InitPosition[:]
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
        self.MaskSet=[mask1,mask2,mask3,mask3,mask2,mask1]
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
        def flip(a):
            #flip 2d array along main diagonal
            b=np.zeros_like(a)
            for i in range(a[0].size):
                for j in range(a[0].size):
                    b[j,i] = a[i,j]
            return b
        """This function creates the 2d matrix of which element interact with which neighbour with which coefficient"""
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
                patternP[i]=gammaLongRange*math.e**(z/self.LongRangeInteractionLength[i])
                delta+=1
            else:
                name1=self.MaterialName[i-1]
                delta=0
                z=-delta*self.MLThickness[i]
                patternP[i]=gammaLongRange*math.e**(z/self.LongRangeInteractionLength[i])
                delta+=1
                index+=1
        index=self.LayerNumber[-1]+1
        delta=0
        for i in reversed(range(self.MaterialName.size)):
            if index-self.LayerNumber[i]==1:
                z=delta*self.MLThickness[i]
                patternM[i]=math.e**(z/self.LongRangeInteractionLength[i])
                delta-=1
            else:
                delta=0
                z=delta*self.MLThickness[i]
                patternM[i]=math.e**(z/self.LongRangeInteractionLength[i])
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
        #for i in range(self.B.size):
        #    for j in range(self.B.size):
        #        print(i, j, self.NeighboursWeight[i,j])
        return 0

    def CalculateM(self):
        self.M=self.MaterialSaturationM*self.B
        return 0
    def UpdateHexi(self):
        #effective field calculaion. Not sure about the volume normalization
        #Hexi            =   self.MLThickness*Hexi
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
                M2          =   self.M[self.NeighboursWeightMask[i]]
                theta       =   self.ThetaM[self.NeighboursWeightMask[i]]-self.ThetaM[i]
                const       =   self.NeighboursWeight[i,self.NeighboursWeightMask[i]]
                aaa=self.Dot(M2,1,theta,const)
                LongRangeExchangeEnergy[i]=np.sum(aaa)
            self.LongRangeExchange       =   LongRangeExchangeEnergy #actually field but who cares
        return 0
#    def UpdateHexNOld(self,OldTheta=None):
#        """previous version of exchange with a regular exchange and RKKY-ish exchange with scalable J"""
#        """LongRangeExchange is a new variable that replaced the RKKY related component as the rkky-ish naming is incorrect"""
#        Mip1            =   np.roll(self.M,-1)
#        Mim1            =   np.roll(self.M,1)
#        Mip2            =   np.roll(self.M,-2)
#        Mim2            =   np.roll(self.M,2)
#        if self.RKKYactive:
#            Bp1            =   np.roll(self.B,-1)
#            Bm1            =   np.roll(self.B,1)
#            Bp2            =   np.roll(self.B,-2)
#            Bm2            =   np.roll(self.B,2)
#            RKKYJip1            =   self.RKKYP1*Bp1
#            RKKYJim1            =   self.RKKYM1*Bm1
#            RKKYJip2            =   self.RKKYP2*Bp2
#            RKKYJim2            =   self.RKKYM2*Bm2
#
#        Jip1            =   self.GammaP1
#        Jim1            =   self.GammaM1
#        Jip2            =   self.GammaP2
#        Jim2            =   self.GammaM2
#        #effective field calculaion. Not sure about the volume normalization
#        if type(OldTheta)!=type(np.array([])):
#            dThetap1        =   np.roll(self.ThetaM,-1)-self.ThetaM
#            dThetam1        =   np.roll(self.ThetaM,1) -self.ThetaM
#            dThetap2        =   np.roll(self.ThetaM,-2)-self.ThetaM
#            dThetam2        =   np.roll(self.ThetaM,2) -self.ThetaM
#        else:
#            dThetap1        =   np.roll(self.ThetaM,-1)-OldTheta
#            dThetam1        =   np.roll(self.ThetaM,1) -OldTheta
#            dThetap2        =   np.roll(self.ThetaM,-2)-OldTheta
#            dThetam2        =   np.roll(self.ThetaM,2) -OldTheta
#        Hex1            =   (self.Dot(Mim1,1,dThetam1,Jim1)+self.Dot(Mip1,1,dThetap1,Jip1))
#        #Hex1            =   self.MLThickness*Hex1
#        Hex2            =   (self.Dot(Mim2,1,dThetam2,Jim2)+self.Dot(Mip2,1,dThetap2,Jip2))
#        #Hex2            =   self.MLThickness*Hex2
#        if self.RKKYactive:
#            HexRKKY1            =   (self.Dot(Mim1,1,dThetam1,RKKYJim1)+self.Dot(Mip1,1,dThetap1,RKKYJip1))
#            HexRKKY2            =   (self.Dot(Mim2,1,dThetam2,RKKYJim2)+self.Dot(Mip2,1,dThetap2,RKKYJip2))
#            HRKKY            =   HexRKKY1+HexRKKY2
#            self.HRKKY       =   HRKKY
#        else:
#            self.HRKKY       =   np.zeros_like(self.B)
#        HexN            =   Hex1+Hex2
#        self.HexN       =   HexN
#        return 0

    def UpdateHzz(self):
        #effective field calculaion. Not sure about the volume normalization
        Hz              =   self.Dot(self.Field,1,self.ThetaM-self.FieldDirection,1) #Zeeman with external field
        Hsup            =   self.Dot(self.MaterialExtraField,1,self.ThetaM-self.MaterialExtraFieldDirection,1) # Zeeman with supplementary field
        self.Hezz       =   Hz+Hsup
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
        self.IterateMagnetisation(50)
        Told=np.copy(self.ThetaM)
        for i in range(self.NumberOfSteps):
            self.MinimizeOrientation()
            self.IterateMagnetisation()
            dtheta=self.ThetaM-Told
            Told=np.copy(self.ThetaM)
            cheatMask=self.B>1e-3
            if i>5 and np.any(np.abs(dtheta)>1e-2):
                cheatMaskM=self.B>1e-3
                cheatMaskT1=np.abs(dtheta)>1e-2
                cheatMaskT2=np.abs(dtheta)<=0.2
                k=0.87*(1+0.07*cheatMaskT2)
                self.ThetaM[cheatMask]=self.ThetaM[cheatMask]+k[cheatMask]*dtheta[cheatMask] # 0,87 magic number do not touch!!!
            #print(i, self.ThetaM[2], self.ThetaM[-2])
        self.NormalizeThetaM()
        self.IterateMagnetisation()
        s1="System simulation for "
        s2="T="+str(self.Temperature)
        s3=" H="+str(self.Field)
        s4="is complete"
        print(colored(s1, 'blue'), colored(s2, 'red'),colored(s3, 'red'),colored(s4, 'green'))


    def MinimizeOrientation(self):
        for i in range(100):
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
                dSpm[dSpm==0]=1e-20
                shift3=(-Sm*self.delta/dSpm)-self.delta/2
                #calculate total shift
                shift=np.zeros_like(self.ThetaM)
                shift[C1]=shift1[C1]
                shift[C2]=shift2[C2]
                shift[C3]=shift3[C3]
                self.ThetaM[M]=self.ThetaM[M]+shift[M]
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
        return np.full(self.MaterialName.shape,const,dtype=np.double)

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
