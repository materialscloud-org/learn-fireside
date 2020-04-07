# Convergence tests

When running DFT calculations, several approximation have to be present in order to run the code on a computer.

In order to determine whether the accuracy of the desired results is being affected by these approximations, a series of convergence tests has to be performed.  
The basic idea behind them is to vary a parameter inherent to the accuracy of our calculation and observe how certain quantities vary with it. When these variations are below a threshold that represent the desired output accuracy, we say that our calculation is "converged" with respect to that parameter.

For more details on what are each approximations, refer to the documentation of each subsection.

- 1: [Cutoff convergence vs Total energy](1_ecut_vs_etot/README.md)
- 2: [Cutoff convergence vs Forces](2_ecut_vs_forces/README.md)
- 3: [K-points convergence vs Total energy](3_kpt_vs_etot/README.md)
- 4: [K-points convergence vs Forces](4_kpt_vs_forcs/README.md)

