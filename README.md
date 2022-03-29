# Moth
This program is designed to simulate a magnetostatic behavior of the magnetization of the stack of thin films of magnetic material with exchange interaction between the layers. The approach of this method is next:
- Each layer of the material is split into a number of monolayers, according to the thickness of the layer and the crystal structure of the material.
-Each monolayer is affected by the effective field, that consist of the contribution of the external magnetic field and exchange field
- The exchange field, that acts on the monolayer, consists of the contributions of the exchange fields from the neighboring monolayers and the internal (intra-monolayer) exchange field.
- An additional static field may be declared for a specific layer, the purpose of this field is to simulate the exchange bias effect. This field is also added to the total effective field of the monolayers, where it is active.
- The magnetization of the monolayer is calculated using a self-consistent Brillouin function.
- For the current solution, it is assumed that the system has strong easy-plane shape anisotropy, thus the direction of the magnetization of the monolayer may rotate only in the plane.
- The direction of the magnetization of the monolayer is found by the minimization of the energy of the monolayer in a static environment with a gradient descending method.
- The exchange interaction between two layers may be calculated in two ways:
- Short-range exchange. This method calculates the exchange field only from n-2, n-1, n, n+1, n+2
- Long-range exchange. This method calculates the exchange of kind "all-to-all" where the amount of involved monolayers is defined by the exchange length parameter. The penetration profile of the weight coefficient of the interlayer exchange is defined by the law e^-z/l where z is the coordinate in nm and l is the penetration length. - - The simulations may be done at variable temperatures, both lower and higher than the Curie temperature of layers.


To run the program, use the following command:
python3 path-to-Moth/Moth.py path-to-config/config-name.py CPU

