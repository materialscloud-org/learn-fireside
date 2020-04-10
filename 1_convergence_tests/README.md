# Convergence tests for input parameters

In this section you will perform a series of basic convergence tests on certain input parameters.

When running DFT calculations, several approximation have to be present in order to run the code on a computer.

In order to determine whether the accuracy of the desired results is being affected by these approximations, a series of convergence tests has to be performed.  
The basic idea behind them is to vary a parameter inherent to the accuracy of our calculation and observe how certain quantities vary with it. When these variations are below a threshold that represent the desired output accuracy, we say that our calculation is "converged" with respect to that parameter.

You might rightfully ask: "Why compromise at all and not use extremely high values for this parameters?". The answer to this is TIME.  
You will notice while doing the exercises that an higher value of a convergence parameter will also result in an longer execution time of your code.
Computational resources have a cost and most importantly are usually limited, hence you always want to aim to squeeze all the possible calculation out of them, while still obtaining physically relevant results.

For more details on each approximation, refer to the documentation of each subsection and the [handouts](../files/handouts.pdf).

# Exercises

  a. [Convergence of total (absolute) energies with respect to cutoff energies](a_ecut_vs_etot/README.md)  
  b. [Convergence of forces with respect to cutoff energies](b_ecut_vs_forces/README.md)  
  c. [Convergence of the total (absolute) energies with respect to the size of the k-points mesh](c_kpt_vs_etot/README.md)  
  d. [Convergence of forces with respect to the size of the k-points mesh](d_kpt_vs_forces/README.md)  
  e. [Convergence of the total energy differences with respect to energy cutoff](e_ecut_vs_ediff/README.md)  

[BACK TO INDEX](../README.md)