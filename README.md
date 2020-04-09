# learn-fireside

This is a tutorial for density-functional theory (DFT) calculations using the open-source [Quantum ESPRESSO] distribution (https://www.quantum-espresso.org/)(QE)[1,2].

In each subfolder you will find the required instructions to run the example exercise. All the required input and pseudopotential files can be found under the ```files``` folder.

The SSSP pseudopotentials (PPs) files can be downloaded from the [Materials Cloud (https://www.materialscloud.org/discover/sssp/table/efficiency#sssp-license). Other sites providing PPs are [pseudodojo](http://www.pseudo-dojo.org/) and [Quantum ESPRESSO website](https://www.quantum-espresso.org/pseudopotentials). The input files required to run the calculations are provided within this repository.

All codes required to run the examples are already installed in the Quantum Mobile (see below), a virtual machine (VM) that can run on any Windows, Mac, or Linux laptop/desktop. Both the codes and Quantum Mobile are open source. 

# Using the Quantum Mobile Virtual Machine

The setup of the Quantum Mobile requires you to download the [Quantum Mobile image](https://github.com/marvel-nccr/quantum-mobile/releases/) (we use the v20.03.1 release) and the open-source Virtual Box (VBox) virtualizaton software.   In order to import the image inside VBox, please refer to [this documentation](https://docs.oracle.com/cd/E26217_01/E26796/html/qs-import-vm.html).

NOTE: If you are running this tutorial on a laptop, beware that some manufacturers disable the Virtualization technology at the BIOS level. This feature can be reactivated, but we would advise against doing it yourself unless you know exactly what you are doing, and it might be wiser to install Quantum ESPRESSO natively on your machine - for this, see instructions at https://www.quantum-espresso.org/Doc/user_guide.pdf

# Convergence tests

In exercises 1 through 5 you will perform a series of basic convergence tests on the core computational input parameters for a proper DFT calculations.

In particular, in order to determine whether the accuracy of the desired results is being affected by your numerical approximations, a series of convergence tests has to be performed. The basic idea behind them is to vary a parameter inherent to the accuracy of the calculation and monitor how certain quantities vary with it. When these variations are below a threshold that represent the desired output accuracy, we say that our calculation is "converged" with respect to that parameter.

You might rightfully ask: "Why compromise at all and not use extremely high values for all the parameters?". The answer to this is TIME, and MEMORY. You will notice while doing the exercises that a higher value of a convergence parameter will also result in an longer execution time of your code. Computational resources have a cost and most importantly are usually limited, hence you always want to aim to have physically relevant results at the minimum meaningful cost.

For more details on each approximation, refer to the documentation of each subsection and the [handouts](files/handouts.pdf).

# Computing mechaical properties

In exercises 6 and 7 you will compute a series of mechanical properties of a material (NaCl).

# Exercises

0. [Launching a PWscf calculation](0_initial_tests/README.md)
1. [Cutoff convergence vs Total energy](1_basic_convergence_ecut_vs_etot/README.md)
2. [Cutoff convergence vs Forces](2_basic_convergence_ecut_vs_forces/README.md)
3. [K-points convergence vs Total energy](3_basic_convergence_kpt_vs_etot/README.md)
4. [K-points convergence vs Forces](4_basic_convergence_kpt_vs_forces/README.md)
5. [Cutoff convergence vs energy differences](5_basic_convergence_ecut_vs_ediff/README.md)
6. [Lattice parameter](6_mechanical_properties_lattice_param/README.md)
7. [Elastic constants](7_mechanical_properties_elastic_constants/README.md)

## Bibliography
1. P. Giannozzi, S. Baroni, N. Bonini, M. Calandra, R. Car, C. Cavazzoni, D. Ceresoli, G. L. Chiarotti, M. Cococcioni, I. Dabo, et al., Journal of physics: Condensed matter 21, 395502 (2009).
2. P. Giannozzi, O. Andreussi, T. Brumme, O. Bunau, M. B. Nardelli, M. Calandra, R. Car, C. Cavazzoni, D. Ceresoli, M. Cococcioni, et al., Journal of Physics: Condensed Matter 29, 465901 (2017).
