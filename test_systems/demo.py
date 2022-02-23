FolderName          =   "Demo-profiles" #Name of the subfolder to dump profiles of the magnetization of the system
                                        # at each point of field and temperature
                                        
Hmin,Hmax,Hsteps    =   -0.15,   0.15,   96 #Minimum field [T], maximum field [T], number of steps in filed.

FieldDirection      =   0 # Direction of the external magnetic field [deg]

Tmin,Tmax,Tsteps    =   320,     320,    1 #Minimum temperature [K], maximum temperature [K], number of steps in temperature .

NumberOfSteps       =   24000   #Maximum number of iterations to be done. 
                                #The exit from the iteration loop is possible by two conditions 
                                # – either dM<1e-7 AND dFi<1e-6 are met or the maximum number of iterations is reached
                                # if abovementioned conditions for dM and dFi are met immediately at start of the simulation,
                                # additional 21 iterations will be done just  in case.

Acceleration        =   1.5     #During the gradient descent, the angle of the magnetization of one monolayer
                                # is changed not on dFi as calculated by the method, but on dFi*Acceleration. 
                                # 1.5 is a maximum number before algorithm goes unstable.
                                # For some systems this parameter must be set to 1.0 as the algorithm may go crazy even at 1.5.
                                #This parameter is chosen experimentally.
                                 
DeleteFlag          =   True    #Clear the subfolder with the magnetization profiles.
                                #Set it to False if the flag ReusePreviousResults is True.  

ReusePreviousResults=   False   #Reuse the previously calculated data. 
                                #At first the program looks into the "FolderName" subfolder and check 
                                # if there are a solution for given H and T, if yes then it will be used as initial state of the system, 
                                # if no then few nearest neighbours on H vs T grid will be checked 
                                # and if found they will be reused as initial state of the system. 
                                # If no previous solution found the system will be initialized in the state 
                                # defined in StructureParameters section.
                                #I strongly recommend to not reuse the previous solution and set ReusePreviousResults to False, as 
                                # the end result may vary from case to case and this function need to be extra validated. 
                                # If used, extra verification is required to ensure that the solution is correct*
                                #*correct - on its way and close to the global minima of the energy of the system. 
                                
#the structural parameters of the system to be simulated
StructureParameters={
            "MaterialThickness":            (0.3,       1.2,        0.3,        ),  #thickness of the layer of magnetic material [nm]
                                                                                    #The minimal thickness of the layer is 2 monolayers.
                                                                                    #Layer of magnetic material with single monolayer
                                                                                    # thickness may be initialized though. It will lead to
                                                                                    # the case when the nearest and next-nearest monolayers
                                                                                    # are different materials.
                                                                                    # I have no  idea what will happen then... 
            
            "MLThickness":                  (0.15,      0.15,       0.15,       ),  #thickness of the atomic monolayer [nm]. For BCC iron it is 0.15 nm 
            
            "ZeemanThickness":              (4.0,       1.0,        4.0,        ),  #this parameter is a way to "cheat" a bit and decrease the calculation time. 
                                                                                    #The effective field that acts on the monolayer normally equal to 
                                                                                    # Heff=Hzeeman+Hexchange, this coefficient modifies effective field
                                                                                    # as: Heff=ZeemanThickness*Hzeeman+Hexchange. 
                                                                                    # The value of ZeemanThickness different from 1.0 
                                                                                    # MUST ONLY be used in the case of strong ferromagnetic layer 
                                                                                    # at temperature far below its Curie temperature. 
                                                                                    # The logic behind this coefficient is next: 
                                                                                    # as there will not be any behavioral features inside 
                                                                                    # the strong ferromagnetic layer, we can not simulate 
                                                                                    # the whole thickness of this layer, but only 2 monolayers of it, 
                                                                                    # in bigger Zeeman field, thus saving the computation time. 
            
            "MaterialName":                 ("Fe",      "FeCr",    "Fe",       ),  #Name of the material of the magnetic layer,
                                                                                    # you are free to choose anithing you like, be creative!
                                                                                    # If you want to simulate e.g. how two layers of the same material
                                                                                    # are interacting with each other via some interlayer exchange
                                                                                    # that is different from the internal exchange of the material 
                                                                                    # (e.g. RKKY interaction in Fe-Cr-Fe stack) then 
                                                                                    # two identical materials are need to be created. 
                                                                                    # Otherwise two layers of the same material will be handled 
                                                                                    # as single uniform layer. 
            
            "MaterialS":                    (1,         1,          1,          ),  #This parameter corresponds to the value of the spin 
                                                                                    #in the Brillouin function. 
                                                                                    # I have no idea what this means in terms of monolayer approach,
                                                                                    # if YOU know: add the comment or smth.
                                                                                    
            "MaterialExtraField":           (0.1,      0,          0,          ),  # additional field [T] that may be applied 
                                                                                    # to the selected layer of the material, 
                                                                                    # designed specifically to simulate the layer with the exchange bias.
                                                                                    
            "MaterialExtraFieldDirection":  (0,         0,          0,          ),  # The direction of the additional magnetic field [deg].
            
            "MaterialSaturationM":          (1700.0,    778.5,      1700.0,     ),  #Saturation magnetisation of the material of each layer [emu/cm3]
            
            "CurieTemperature":             (0,         0,          0,          ),  #placeholder, not used in the calculations
            
            "GammaCoefficient":             (0.86,      0.86,       0.86,       ),  #The direct (or short range) exchange field in the algorithm
                                                                                    #is calculated as follows:
                                                                                    # Hex=n*J0+k*J0/GammaCoefficient+t*J0
                                                                                    # where:
                                                                                    # n - is a number of neighbours inside the monolayer
                                                                                    # for BCC Fe, n=4, (2st-nearest)
                                                                                    # t - amount of neighbours in i+2 and i-2 neighbouring monolayers
                                                                                    # for the BCC Fe 1 neighbour in i+1 and 1 in i-1 (2nd nearest)
                                                                                    # k - is a number of neighbours in i+1 and i-1 neighbouring monolayers
                                                                                    # for the BCC Fe there are 4 neighbours in i+1 and 4 in i-1 monolayers
                                                                                    # because those atoms are spatially closer to the central atom 
                                                                                    # #the exchange between them should be higher. 
                                                                                    # #Thus the exchange constant is scaled up on the 1/GammaCoefficient 
                                                                                    
            "InitPosition":                 (80.0,      -80.0,      -80.0,      ),  #initial position of the magnetization of each layer of the material.
                                                                                    # The properly guessed position may accelerate the solution a bit.
            
            "InitB":                        (0.75,      0.74,       0.75,       ),  #initial value of the Brillouin function, 
                                                                                    #it seems that it does not effect the solution much
                                                                                    # and does not change the convergence speed.
                                                                                    
            "LongRangeInteractionLength":   (0.15,      0.45,       0.15,       ),  #The length of the involvement of the monolayers 
                                                                                    # inside the layer into the interlayer exchange interaction. 
                                                                                    # The profile of the penetration is e^(-z/l) where z is 
                                                                                    # the coordinate and l is the LongRangeInteractionLength
                                                                                    #It is possible to see the sparce matrix of the
                                                                                    # long range exchange interaction using the
                                                                                    # Moth-exchange-profile.py script
            
            "LongRangeExchangeFlag":         False,     # This flag indicates if the interlayer exchange interaction will be calculated
                                                        # as a "regular"/"direct/"short range" exchange with 1-st ad 2-nd neighbouring layers, or
                                                        # as "some amount of edge monolayers in layer 1" have exchange interaction
                                                        # with "some amount of edge monolayers in layer 2"
                                                        # with exponentially decaying exchange constants between them.
                                                        # If set to False the parameter  LongRangeInteractionLength is ignored.
            
            "InitPositionSingle":            10,        # legacy, not used anymore. It was the same as InitPosition, but for the same angle for all layers
            
            "PeriodicBoundaryConditions":    False      # If True, then periodic boundary conditions are used.
                                                        # This option is need to be tested, as I didn't check if it works properly.
            }
# direct exchange pairvise interaction constants
MaterialExchange={
            "FeCr-FeCr"     :0.03,
            "FeCr-Fe"       :-0.002,
            "Fe-Fe"         :0.3,
            "Fe-FeCr"       :-0.002 #<---- please observe, no coma after last element of dictionary
            }       # Pairvise exchange between te materials. The value of the exchange constant from material A to material B must be equal 
                    # to the value of the exchange constant from material B to material A! 
                    # For any pairvise exchange between material A and B, the notation must strictly follow to the next pattern: "A-B"
                    # The value of the exchange constant from material A to material A indicates the internal exchange of the material,
                    # and basically defines its Curie temperature.
                    # The vavue of the exchange constant from material A to material B indicated the interlayer exchange
                    # The internal exchange of the material is ALWAYS calculated as a direct/short range exchange!
                    # to find the value of the exchange inside the material do next:
                    #   1. Create the config file with one layer of material for which you would like to find the value of the exchange constant,
                    #   2. Find, or agree to some value of the Curie temperature of the material
                    #   3. Find or agree to some value of the magnetization of the material
                    #   4. Set initial value of the material exchange constant
                    #   5. Simulate the MvsT dependence and find the Curie temperature from this data
                    #   6. Change the exchange constant, depending on how different the obtained Curie temperature from expected one
                    #   7. Repeat from 5. untill Tc obtained from the simulations coinside with the expected one.
                    #   8. Cheer up yourself with a nice cup of tea with milk!

LongRangeExchange={
            "FeCr1-FeCr2"  :-0.0014,
            "FeCr1-Fe"     :-0.002,
            "FeCr2-FeCr1"  :-0.0014,
            "FeCr2-Fe"     :-0.002,
            "Fe-FeCr1"     :-0.002,
            "Fe-FeCr2"     :-0.002
            }       # This dictionary contains the set of pairvise exchange interaction for the calculation of the long range exchange.
                    # Those parameters are only used when the flag LongRangeExchangeFlag is True.
                    # This interaction will be only calculated between different layers of different materials.
                    # No meter how big the LongRangeInteractionLength parameter is, the long range exchange will be always limited to the thickness 
                    # of the nearest layer*.
                    # * play with the structural parameters and check the sparse matrix, you will get it. 
        
        #----------------!!!! CAUTION !!!!---------------------
        # Be carefull when you are defining the long range exchange. 
        # The long range exchange and the short range exchange will be calculated simultaneously. Thus if you want to simulate only a long-range interaction,
        # then the short range exchange constants must be set to 0.0
         
        
        
        # The program is in early stge of development, thus no reliable fool-proof mechanism is implemented regarding the analysis of input parameters.
        # Thus in is beter to leave all variables defined in the config file, even if they are not used in the analysis.