# learn-fireside

This is a tutorial for density-functional theory (DFT) calculations using the open-source [Quantum ESPRESSO distribution](https://www.quantum-espresso.org/) (QE)[1,2].

In each subfolder you will find the required instructions to run the example exercise. All the instruction (Handouts) and required input and pseudopotential files can be found under the ```files``` folder.

The SSSP pseudopotentials (PPs) files can be downloaded from the [Materials Cloud](https://www.materialscloud.org/discover/sssp/table/efficiency#sssp-license). Other sites providing PPs are [pseudodojo](http://www.pseudo-dojo.org/) and [Quantum ESPRESSO website](https://www.quantum-espresso.org/pseudopotentials). The input files required to run the calculations are provided within this repository.

All codes required to run the examples are already installed in the Quantum Mobile (see below), a virtual machine (VM) that can run on any Windows, Mac, or Linux laptop/desktop. Both the codes and Quantum Mobile are open source. 

# Using the Quantum Mobile Virtual Machine

The setup of the Quantum Mobile requires you to download the [Quantum Mobile image](https://github.com/marvel-nccr/quantum-mobile/releases/) (we use the v20.03.1 release) and the open-source Virtual Box (VBox) virtualizaton software.   In order to import the image inside VBox, please refer to [this documentation](https://docs.oracle.com/cd/E26217_01/E26796/html/qs-import-vm.html).

NOTE: If you are running this tutorial on a laptop, beware that some manufacturers disable the Virtualization technology at the BIOS level. This feature can be reactivated, but we would advise against doing it yourself unless you know exactly what you are doing, and it might be wiser to install Quantum ESPRESSO natively on your machine - for this, [see instructions](https://www.quantum-espresso.org/Doc/user_guide.pdf)

# Exercises

 - [Exercise 0](0_initial_tests/README.md): Running a PWscf example and obtaining the total energy
 - [Exercise 1](1_convergence_tests/README.md): Convergence tests for input parameters
 - [Exercise 2](2_lattice_param_bulk_modulus/README.md): Determination of the equilibrium lattice length and bulk modulus
 - [Exercise 3](3_elastic_constants/README.md): Determination of the elastic constants

## Bibliography
1. P. Giannozzi, S. Baroni, N. Bonini, M. Calandra, R. Car, C. Cavazzoni, D. Ceresoli, G. L. Chiarotti, M. Cococcioni, I. Dabo, et al., Journal of physics: Condensed matter 21, 395502 (2009).
2. P. Giannozzi, O. Andreussi, T. Brumme, O. Bunau, M. B. Nardelli, M. Calandra, R. Car, C. Cavazzoni, D. Ceresoli, M. Cococcioni, et al., Journal of Physics: Condensed Matter 29, 465901 (2017).
