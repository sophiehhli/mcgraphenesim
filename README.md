# Monte Carlo Phonon and Electron Graphene Simulation 
Simulation of ballistic phonon and electron trajectories in graphene flakes. 

## Background
The ability to detect single photons has applications in a wide range of disparate fields. One approach for pushing the limits of single-photon detector (SPD) energy resolution is to exploit the temperature rise in a low-heat capacity material upon absorption of a photon. Due to its attractive electrical, thermal and material properties, graphene has emerged as an exciting candidate for thermal SPDs. A collaboration between the research groups of Prof. Michael Roukes and Prof. Stevan Nadj-Perge has developed a novel graphene-based thermal detector. The behavior of phonons on the graphene flake of the SPD in the low-temperature, boundary-scattering regime was simulated, to further understand the nature of the temperature distribution across the graphene flake. By way of Monte Carlo techniques, the code of which is in this git hub repository, we have quantified the effect of diffuse and specular surface scattering for circular and rectangular flake geometries. 

The work so far was adapted from the Monte Carlo simulations in ["Phonon radiative heat transfer and surface scattering" by Tom Klitsner et. al.(1987)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.38.7576)

## Authors 
Student: Sophie Li 

Mentors: Michael Roukes, Stevan Nadj-Perge, and Raj Katti 

Robert L. Blinkenberg SURF Fellow

## Contents
[```boundary.py```](https://github.com/sophiehhli/mcgraphenesim/blob/master/boundary.py) Classes that define the boundary of the graphene flake 

[```contact.py```](https://github.com/sophiehhli/mcgraphenesim/blob/master/contact.py) Classes that define and contacts/leads to the flake, for instance, source, drain or thermometer leads 

[```grad.py```](https://github.com/sophiehhli/mcgraphenesim/blob/master/grad.py) Functions to calculate gradient at a point 

[```interaction.py```](https://github.com/sophiehhli/mcgraphenesim/blob/master/interaction.py) Class for Intersection object, functions handeling interactions

[```point.py```](https://github.com/sophiehhli/mcgraphenesim/blob/master/point.py) Point class, object with position and direction, either phonon or electron 

[```plotfunc.py```](https://github.com/sophiehhli/mcgraphenesim/blob/master/plotfunc.py) Functions to plot various outputs of the simulation 

[```mcgraphene.py```](https://github.com/sophiehhli/mcgraphenesim/blob/master/mcgraphene.py) Script to be executed, performs main loop of the simulation, point from which to call plotting functions. 
