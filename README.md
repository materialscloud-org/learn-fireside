# learn-fireside

This is a tutorial for Density Functional Theory(DFT) calculation using [Quantum ESPRESSO](https://www.quantum-espresso.org/)(QE)[1,2]

In each subfolder you will find the required material to run the example exercise and the instruction as a README.md file which can be viewed directly from github

1. [Basic convergence tests](1_basic_convergence/README.md)
2. [Mechanical properties](2_mechanical_properties/README.md)

All codes required to run the examples are already installed within the provided virtual machine (VM).  
The SSSP pseudopotentials (PPs) files required to run the exercises can be found on [Materials Cloud](https://www.materialscloud.org/discover/sssp/table/efficiency#sssp-license).
Other sites providing PPs are [pseudodojo](http://www.pseudo-dojo.org/) and [Quantum ESPRESSO website](https://www.quantum-espresso.org/pseudopotentials).  
The input files required to run the calculations are provided within this repository.

The setup of the VM requires you to download the latest [Quantum Mobile image](https://github.com/marvel-nccr/quantum-mobile/releases/) and VBox version 6.1.  
In order to import the image inside VBox, please refer to [this documentation](https://docs.oracle.com/cd/E26217_01/E26796/html/qs-import-vm.html)

NOTE: If you are running this tutorial on a laptop, beware that some manufacturers disable the Virtualization technology on a BIOS level. While the feature can be reactivated, we would advise against doing it yourself unless you know what you are doing.

## Bibliography
1. P. Giannozzi, S. Baroni, N. Bonini, M. Calandra, R. Car, C. Cavazzoni, D. Ceresoli, G. L. Chiarotti, M. Cococcioni, I. Dabo, et al., Journal of physics: Condensed matter 21, 395502 (2009).
2. P. Giannozzi, O. Andreussi, T. Brumme, O. Bunau, M. B. Nardelli, M. Calandra, R. Car, C. Cavazzoni, D. Ceresoli, M. Cococcioni, et al., Journal of Physics: Condensed Matter 29, 465901 (2017).