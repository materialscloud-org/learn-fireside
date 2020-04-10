# learn-fireside

This is a tutorial for Density Functional Theory(DFT) calculation using [Quantum ESPRESSO](https://www.quantum-espresso.org/)(QE)[1,2]

In each subfolder you will find the required instruction to run the example exercise.  
All the required input and pseudopotential files can be found under the ```files``` folder.

All codes required to run the examples are already installed within the provided virtual machine (VM).  
The SSSP pseudopotentials (PPs) files can be acquired from [Materials Cloud](https://www.materialscloud.org/discover/sssp/table/efficiency#sssp-license).
Other sites providing PPs are [pseudodojo](http://www.pseudo-dojo.org/) and [Quantum ESPRESSO website](https://www.quantum-espresso.org/pseudopotentials).  
The input files required to run the calculations are provided within this repository.

# Using the Quantum Mobile Virtual Machine

The setup of the VM requires you to download the latest [Quantum Mobile image](https://github.com/marvel-nccr/quantum-mobile/releases/) and VBox version 6.1.  
In order to import the image inside VBox, please refer to [this documentation](https://docs.oracle.com/cd/E26217_01/E26796/html/qs-import-vm.html)

NOTE: If you are running this tutorial on a laptop, beware that some manufacturers disable the Virtualization technology on a BIOS level. While the feature can be reactivated, we would advise against doing it yourself unless you know what you are doing.

# Exercises

 - [Exercise 0](0_initial_tests/README.md): Running a PWscf example and obtaining the total energy
 - [Exercise 1](1_convergence_tests/README.md): Convergence tests for input parameters
 - [Exercise 2](2_lattice_param_bulk_modulus/README.md): Determination of the equilibrium lattice length and bulk modulus
 - [Exercise 3](3_elastic_constants/README.md): Determination of the elastic constants

6. [Lattice parameter](6_mechanical_properties_lattice_param/README.md)
7. [Elastic constants](7_mechanical_properties_elastic_constants/README.md)

## Bibliography
1. P. Giannozzi, S. Baroni, N. Bonini, M. Calandra, R. Car, C. Cavazzoni, D. Ceresoli, G. L. Chiarotti, M. Cococcioni, I. Dabo, et al., Journal of physics: Condensed matter 21, 395502 (2009).
2. P. Giannozzi, O. Andreussi, T. Brumme, O. Bunau, M. B. Nardelli, M. Calandra, R. Car, C. Cavazzoni, D. Ceresoli, M. Cococcioni, et al., Journal of Physics: Condensed Matter 29, 465901 (2017).