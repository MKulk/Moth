# Moth
This program is designed to simulate a magnetostatic behaviour of the magnetization of the stack of thin films of magnetic material with exchange interaction between the layers. 
The approach of this method is next:
- Each layer of the material is splitted on a number of the monolayers, according to the thickness of the layer and the crystal structure of the material.
- Each monolayer is affected by the effective field, that consist of the contribution of the external magnetic field and exchange field
- The exchange field, that acts on the monolayer, consist of the contributions of the exchange fields from the neighbouring monolayers and internal (intramonolayer) exchange field.
- Additional static field may be declared for specific layer, the purpose of this field is to simulate exchnage bias effect. This field is also added to total effective field of the monolayers, where it is active.
- The magnetization of the monolayer is calculated using a self-consystent Brilluoin function.
- For current solution it is assumed that the system have strong easy-plane shape anisotropy, thus the direction of the magnetisation of the monolayer may rotate only in plane.
- The direction of the magnetization of the monolayer is found by the minimization of the energy of the monolayer in static environment with gradient descending method.
- The exchange interaction between two layers may be calculated in two ways:
  * Short range exchange. This method calculates the exchange field only from n-2, n-1, n, n+1, n+2
  * Long range exchange. This method calculates the exchange of kind "all-to-all" where the amount of invalved monolayers is defined by the exchange length parameter. The penetration profile of the weight coefficient of the interlayer exchange is defined by the law e^-z/l where z is the coordinate in nm and l is the penetration length. 
The simulations may be done at variable temperature, both lower and higher than the Curie temperature of layers. The    
