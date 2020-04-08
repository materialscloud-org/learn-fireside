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

# Convergence tests

In exercises 1 through 5 you will perform a series of basic convergence tests on certain input parameters.

When running DFT calculations, several approximation have to be present in order to run the code on a computer.

In order to determine whether the accuracy of the desired results is being affected by these approximations, a series of convergence tests has to be performed.  
The basic idea behind them is to vary a parameter inherent to the accuracy of our calculation and observe how certain quantities vary with it. When these variations are below a threshold that represent the desired output accuracy, we say that our calculation is "converged" with respect to that parameter.

You might rightfully ask: "Why compromise at all and not use extremely high values for this parameters?". The answer to this is TIME.  
You will notice while doing the exercises that an higher value of a convergence parameter will also result in an longer execution time of your code.
Computational resources have a cost and most importantly are usually limited, hence you always want to aim to squeeze all the possible calculation out of them, while still obtaining physically relevant results.

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