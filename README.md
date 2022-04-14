# Moth
This program is designed to simulate magnetostatics in thin films and multilayers of magnetic materials at finite temperature. 

When studying magnetic multilayers one is often interested only in the profile of the magnetization across the thickness of the system. However, in order to obtain nice data at finite temperatures from micromagnetics or atomistic spin dynamics, very large lateral dimensions may be required. This leads to long simulation times, especially close to the critical temperature where the system may still be too small to avoid superparamagnetic behaviour not seen in experiments. In Moth these problems are eliminated as each monolayer is represented by one magnetic moment of variable magnitude, and the temperature is taken into account using a Brillouin function instead of random fluctuations.

Approach
- Each film or layer in the system is split into monolayers, according to its thickness and the crystal structure of the material.
- Each monolayer is subject to an effective field, which consists of contributions from the external magnetic field and the exchange field.
- The exchange field acting on a monolayer consists of inter- and intralayer contributions, from neighbouring monolayers and from interatomic exchange within the monolayer itself.
- Additional static and layer specific fields may be defined, with the purpose of simulating exchange bias effects. These fields are added to the total effective fields of the relevant monolayers.
- The magnetization of the monolayers is calculated using a self-consistent Brillouin function.
- In the current version it is assumed that the system has strong easy-plane shape anisotropy, thus the magnetization of the monolayers may rotate only in the plane.
- The magnetization direction of a monolayer is found by the minimization of its energy in a static environment using a gradient descending method.
- The exchange interaction between two layers may be calculated in two ways:
  - Short-range exchange. In this mode the exchange interractions reach no further than the second nearest neighbour monolayer.
  - Long-range exchange. In this mode there is no limit to the range of the exchange interractions. The interlayer exchange decays exponentially, J~exp(-z/l), with an exchange length parameter l set by the user.
- The simulations may be done at variable temperatures, both lower and higher than the Curie temperature of the layers.


To run the program, use the following command:

```bash
python3 path-to-Moth/Moth.py path-to-config/config-name.py CPU
```
the last argument "CPU" declares the processing target, available targets are: "CPU", "GPU". For now only "CPU" is working.
