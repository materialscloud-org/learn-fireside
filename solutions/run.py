#!/usr/bin/env python3

'''
Script for running all of the learn-fireside tutorial

Written by Edward Linscott Feb 2021
edwardlinscott@gmail.com
'''


import os
import copy
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import seaborn

import sys
sys.path.append('./ase/')
from ase.io.espresso import read_espresso_in, KEYS, units, read_espresso_out, Espresso, ibrav_to_cell, cell_to_ibrav
from ase import Atoms

seaborn.set_style('darkgrid')
seaborn.set_context('notebook')
CONVERGED_SETTINGS = {}

class Problem:

   def __init__(self, label, master_atoms='../files/NaCl.scf.in', from_scratch=False):

      if isinstance(master_atoms, str):
         assert os.path.isfile(master_atoms), f'{master_atoms} does not exist'
         self.master_atoms = read_espresso_in(master_atoms)
      elif isinstance(master_atoms, Atoms):
         self.master_atoms = master_atoms
      else:
         raise TypeError('master_atoms must be either a string defining the path to an input file, or an ASE Atoms() object')
      self.label = label
      self.master_atoms.calc.directory = f'./{self.label}'
      self.directory = self.master_atoms.calc.directory
      self.calculations = []

      pseudo_dir = master_atoms.rsplit('/', 1)[0] + '/' + self.get_setting('pseudo_dir')
      self.set_setting('pseudo_dir', os.path.abspath(pseudo_dir))
      self.from_scratch = from_scratch
      if self.from_scratch and os.path.isdir(self.directory):
         os.system(f'rm -r {self.directory}')

      if not os.path.isdir(self.directory):
         os.system(f'mkdir {self.directory}')

      # Apply the converged values
      for k, v in CONVERGED_SETTINGS.items():
         self.set_setting(k, v)

   @property
   def settings(self):
      return self.master_atoms.calc.parameters['input_data']

   def get_setting(self, setting, atoms=None):
      if atoms is None:
         atoms = self.master_atoms

      if setting == 'cell_volume':
         return atoms.cell.volume

      for block in atoms.calc.parameters['input_data'].values():
         for key, val in block.items():
            if key == setting:
               return val
      return None

   def set_setting(self, setting, value, atoms=None):
      if atoms is None:
         atoms = self.master_atoms

      if setting == 'orthorhombic_distortion':
         distortion = np.diag([1 + value, 1 - value, 1 + value**2/(1-value**2)])
         atoms.cell = np.dot(atoms.cell.array, distortion)
         atoms.positions = np.dot(atoms.positions, distortion)
      elif setting == 'monoclinic_distortion':
         # This distortion does not lead to a monoclinic distortion aligned with either the b or c axis
         # Therefore to get it into a QE-friendly form, we must reconstruct the cell as per the slides
         distortion = np.array([[1, value/2, 0], [value/2, 1, 0], [0, 0, 1 + value**2/(4-value**2)]])
         cell = np.dot(atoms.cell.array, distortion)
         rel_positions = atoms.get_scaled_positions()
         system = {'ibrav': 12}
         [l1, l2, l3] = [np.linalg.norm(v) for v in cell]
         system['celldm(1)'] = l1
         system['celldm(2)'] = l2/l1
         system['celldm(3)'] = l3/l1
         system['celldm(4)'] = np.dot(cell[0], cell[1])/l1/l2
         _, atoms.cell = ibrav_to_cell(system)
         atoms.cell /= units.Bohr
         atoms.set_scaled_positions(rel_positions)
      elif setting == 'cell_volume':
         scaling_factor = (value/atoms.cell.volume)**(1/3)
         atoms.cell *= scaling_factor
         atoms.positions *= scaling_factor
      elif setting == 'volume_per_atom':
         scaling_factor = (value/atoms.cell.volume*len(atoms))**(1/3)
         atoms.cell *= scaling_factor
         atoms.positions *= scaling_factor
      elif setting == 'kpts':
         atoms.calc.parameters['kpts'] = [value for _ in range(3)]
      else:
         for block_name, block in KEYS.items():
            for key in block:
               if key.split('(')[0] == setting.split('(')[0]:
                  atoms.calc.parameters['input_data'][block_name][setting] = value
                  return
         raise ValueError(f'{setting} is not a valid QE setting')
      return

   def run_calculator(self, settings={}):
      atoms = copy.deepcopy(self.master_atoms)

      tag = ''
      for k, v in settings.items():
         if isinstance(v, str):
            tag += f'{k}={v}/'
         else:
            tag += f'{k}={v:g}/'
         self.set_setting(k, v, atoms)
      atoms.calc.directory += '/' + tag

      if not self.from_scratch:
         if os.path.isfile(f'{atoms.calc.label}.pwo'):
            try:
               atoms.calc.results = [c for c in read_espresso_out(atoms.calc.label + '.pwo')][-1].calc.results
            except IndexError:
               self.from_scratch = True
            if not self.from_scratch:
               print(f'Skipping {atoms.calc.label} because it is already complete')
         else:
            self.from_scratch = True

      if self.from_scratch:
         print(f'Running {atoms.calc.label}...', end='', flush=True)
         atoms.calc.calculate()
         print(' done')

      self.calculations.append(atoms.calc)

      return atoms.calc

   def run(self):
      raise NotImplementedError(f'The "{self.__class__.__name__}" class does not have run() implemented')

class ConvergenceProblem(Problem):
   def __init__(self, conv_wrt, conv_threshold, x, extract, *args, **kwargs):
      self.conv_wrt = conv_wrt
      self.conv_threshold = conv_threshold
      self.x = x
      self.extract_quantity_of_interest = extract
      super().__init__(*args, **kwargs)
      self.y = []

   def run_calculations(self):
      for value in self.x:
         settings = {self.conv_wrt: value}
         if self.conv_wrt == 'ecutwfc':
            settings['ecutrho'] = 8*value
         calc = self.run_calculator(settings)
         self.y.append(self.extract_quantity_of_interest(calc))
      self.y = np.array(self.y)

   def extract_quantity_of_interest(self, calc):
      raise NotImplementedError()

   def find_converged_parameter(self):
      self.conv_x, self.conv_y = [(x, y) for i, (x, y) in enumerate(zip(self.x, self.y))
                                  if np.all([np.abs(self.y[i:-1] - self.y[-1]) < self.conv_threshold])][0]

   def plot(self, xlabel, ylabel, filename):
      f, ax = plt.subplots(2,1, sharex=True)

      offset = self.y[-1]

      ax[0].plot(self.x, self.y - offset)
      ax[0].axhspan(-self.conv_threshold, self.conv_threshold, alpha=0.2)
      ax[0].set_ylim([-5*self.conv_threshold, 5*self.conv_threshold])

      ax[1].semilogy(self.x[:-1], abs(self.y[:-1] - offset))
      ax[1].set_xlabel(xlabel)
      ax[1].axhline(self.conv_threshold, color='r', ls='--')

      for a in ax:
         a.plot(self.conv_x, abs(self.conv_y - offset), 'o')
      
      ax[0].set_title(ylabel)

      plt.tight_layout()
      plt.savefig(f'{self.directory}/{filename}.pdf', format='pdf')
      plt.close()

   def run(self):
      self.run_calculations()
      self.find_converged_parameter()

class FiniteDiffConvergenceProblem(ConvergenceProblem):

   def run_calculator(self, settings):
      master_atoms_backup = copy.deepcopy(self.master_atoms)

      # Run the undisplaced calculation
      settings['prefix'] = self.get_setting('prefix') + '_undisplaced'
      calc_undisplaced = super().run_calculator(settings)

      # Displace the second atom
      displacement = np.zeros(self.master_atoms.positions.shape)
      displacement[-1, -1] += 0.05 * self.get_setting('celldm(1)')
      self.master_atoms.translate(displacement)
      settings['prefix'] = self.get_setting('prefix') + '_displaced'

      # Run the displaced calculation
      calc_displaced = super().run_calculator(settings)

      # Restore the master calculator
      self.master_atoms = master_atoms_backup

      # Return a dummy calculator with the total energy difference stored as its "energy"
      calc = Espresso()
      calc.atoms = copy.deepcopy(self.master_atoms)
      calc.atoms.calc = calc
      calc.results['energy'] = calc_displaced.results['energy'] - calc_undisplaced.results['energy']
      return calc

class FittingProblem(Problem):
   def __init__(self, x, fit_wrt, fitting_function, *args, **kwargs):
      self.x = x
      self.y = []
      self.fit_wrt = fit_wrt
      self.fitting_function = fitting_function
      super().__init__(*args, **kwargs)

   def extract_quantity_of_interest(self, calc):
      # Return energy (eV/cell)
      return calc.results['energy']

   def run_calculations(self):
      for value in self.x:
         settings = {self.fit_wrt: value}
         calc = self.run_calculator(settings)
         self.y.append(self.extract_quantity_of_interest(calc))
      self.y = np.array(self.y)

   def reload_calculations(self):
      for value in self.x:
         if isinstance(value, float):
            [calc] = [c for c in self.calculations if abs(self.get_setting(self.fit_wrt, c.atoms) - value) < 1e-9]
         else:
            [calc] = [c for c in self.calculations if self.get_setting(self.fit_wrt, c.atoms) == value]
         self.y.append(self.extract_quantity_of_interest(calc))
      self.y = np.array(self.y)
      self.fit()

   def run(self):
      self.run_calculations()
      self.fit()

   def fit(self):
      if self.guess is None:
         self.params, _ = curve_fit(self.fitting_function, self.x, self.y)
      else:
         self.params, _ = curve_fit(self.fitting_function, self.x, self.y, self.guess)
      return

   def plot(self, xlabel, ylabel, filename):
      f, ax = plt.subplots(1,1)

      ax.plot(self.x, self.y, 'o')
      
      ax.set_xlabel(xlabel)
      ax.set_ylabel(ylabel)

      xmin, xmax = ax.get_xlim()
      xfine = np.linspace(xmin, xmax, 1001)
      ax.plot(xfine, self.fitting_function(xfine, *self.params), label='Energy fit')
      ax.set_xlim([xmin, xmax])

      plt.tight_layout()

      plt.savefig(f'{self.directory}/{filename}.pdf', format='pdf')

      plt.close()

   @property
   def guess(self):
      return None

class BulkModulusProblem(FittingProblem):
   def __init__(self, x, fitting_function, *args, **kwargs):
      # Impose fit_wrt = cell_volume
      super().__init__(x, fit_wrt='cell_volume', fitting_function=fitting_function, *args, **kwargs)

   @property
   def eq_lattice_constant(self):
      default_celldm = cell_to_ibrav(self.master_atoms.cell, self.get_setting('ibrav'))['celldm(1)']
      return default_celldm * (self.eq_lattice_volume / self.master_atoms.cell.volume)**(1/3)

   def plot(self, xlabel, ylabel, filename):
      f, ax = plt.subplots(1,1)

      ax.plot(self.x, self.y, 'o')
      
      ax.set_xlabel(xlabel)
      ax.set_ylabel(ylabel)

      xmin, xmax = ax.get_xlim()
      xfine = np.linspace(xmin, xmax, 1001)
      ax.plot(xfine, self.fitting_function(xfine, *self.params), label='Energy fit')
      ax.set_xlim([xmin, xmax])

      # Converting to enthalpy
      # self.params[1] += 0.101325 * units.GPa # atmospheric pressure
      # ax.plot(xfine, self.fitting_function(xfine, *self.params), label='Enthalpy')

      # Labelling the eq lattice parameter
      text = f'a$_0$ = {self.eq_lattice_constant / units.Bohr:.4f} Bohr'

      # Labelling the bulk modulus
      val = self.bulk_modulus
      val_Rya3 = val / units.Ry * units.Bohr**3
      val_GPa = val / units.GPa
      text += f'\nB = {val_Rya3:.4f} Ry/Bohr^3 = {val_GPa:.4f} GPa'
      if hasattr(self, 'dbulk_modulus'):
         val = self.dbulk_modulus
         val_Rya6 = val / units.Ry * units.Bohr**6
         text += f"\nB' = {val_Rya6:.4f} Ry/Bohr^6"

      # Adding the label
      ax.text(0.05, 0.95, text, ha='left', va='top', transform=ax.transAxes)

      plt.tight_layout()

      plt.savefig(f'{self.directory}/{filename}.pdf', format='pdf')

      plt.close()

class ParabolicBulkModulusProblem(BulkModulusProblem):
   def __init__(self, fitting_function=None, *args, **kwargs):
      def parabola(xdata, a, b, c):
         # A parabola written such that a = d2f/dx2
         return a * xdata**2 / 2 + b * xdata + c
      super().__init__(fitting_function=parabola, *args, **kwargs)

   @property
   def bulk_modulus(self):
      # Returns in units of eV/A^3
      cell_volume = self.master_atoms.cell.volume
      # B = V0 d2E/dV2
      return cell_volume*self.params[0]

   @property
   def eq_lattice_volume(self):
      # The minimum of a parabola ax^2/2 + bx + c is given by x = -b/a:
      # Find the minimum of enthalpy (cf. energy) at 1 atm
      return - (self.params[1] + 0.101325 * units.GPa)/ self.params[0]

class BMBulkModulusProblem(BulkModulusProblem):
   def __init__(self, fitting_function=None, *args, **kwargs):
      def birch_murnaghan(x, e0, v0, b0, db0):
         x23 = (v0/x)**(2/3)
         return e0 + 9*v0*b0/16*(db0*(x23 - 1)**3 + (x23 - 1)**2 * (6 - 4 * x23))
      super().__init__(fitting_function=birch_murnaghan, *args, **kwargs)

   @property
   def guess(self):
      i_mid = len(self.x)//2
      v0_guess = self.x[i_mid]
      e0_guess = self.y[i_mid]
      return [e0_guess, v0_guess, 1, 1]

   @property
   def eq_lattice_volume(self):
      return self.params[1]

   @property
   def bulk_modulus(self):
      # Returns in units of eV/A^3
      return self.params[2]

   @property
   def dbulk_modulus(self):
      # Returns in units of eV/A^3
      return self.params[3]

class ElasticConstantsProblem(FittingProblem):
   def __init__(self, fitting_function=None, *args, **kwargs):
      # Impose fitting function = simple parabola
      def simple_parabola(x, a):
         return a * x**2
      super().__init__(fitting_function=simple_parabola, *args, **kwargs)

   def run_calculations(self):
      super().run_calculations()
      self.y -= self.y[len(self.y)//2]

   def plot(self, xlabel, ylabel, filename):
      f, ax = plt.subplots(1,1)

      ax.plot(self.x, self.y, 'o')
      
      ax.set_xlabel(xlabel)
      ax.set_ylabel(ylabel)

      xmin, xmax = ax.get_xlim()
      xfine = np.linspace(xmin, xmax, 1001)
      ax.plot(xfine, self.fitting_function(xfine, *self.params), label='Energy fit')
      ax.set_xlim([xmin, xmax])

      # Labelling the coefficients
      text = '\n'.join([f'${k}$ = {v / units.Ry * units.Bohr**3:.4f} Ry/Bohr^3 = {v / units.GPa:.4f} GPa' for k, v in
                        self.coefficients.items()])
      ax.text(0.95, 0.95, text, ha='right', va='top', transform=ax.transAxes)

      plt.tight_layout()

      plt.savefig(f'{self.directory}/{filename}.pdf', format='pdf')

      plt.close()


class ElasticConstantsC11C12Problem(ElasticConstantsProblem):
   def __init__(self, bulk_modulus, fit_wrt=None, *args, **kwargs):
      self.bulk_modulus = bulk_modulus
      # Impose fit_wrt = 'orthorhombic_distortion'
      super().__init__(fit_wrt='orthorhombic_distortion', *args, **kwargs)

   @property
   def coefficients(self):
      return {'C_{11}': self.c11, 'C_{12}': self.c12}

   @property
   def c11(self):
      return self.bulk_modulus + 2*self.params[0]/3/self.master_atoms.cell.volume

   @property
   def c12(self):
      return self.bulk_modulus - self.params[0]/3/self.master_atoms.cell.volume

   
class ElasticConstantsC44Problem(ElasticConstantsProblem):
   def __init__(self, fit_wrt=None, *args, **kwargs):
      # Impose fit_wrt = 'monoclinic_distortion'
      super().__init__(fit_wrt='monoclinic_distortion', *args, **kwargs)

   @property
   def coefficients(self):
      return {'C_{44}': self.c44}

   @property
   def c44(self):
      return 2*self.params[0]/self.master_atoms.cell.volume


if __name__ == '__main__':

   # Removing brackets from .in files that ASE struggles with
   os.system('sed -i "s/{//g" ../files/*.in')
   os.system('sed -i "s/}//g" ../files/*.in')

   os.environ['ASE_ESPRESSO_COMMAND'] = 'mpirun -np 4 pw.x -in PREFIX.pwi > PREFIX.pwo'
   from_scratch = False

   global CONVEGED_SETTINGS
   CONVERGED_SETTINGS = {}

   # Define a function to extract the energy from an ASE calculator
   def extract_energy(calc):
      # Return energy (Ry/atom)
      return calc.results['energy']/len(calc.atoms)/units.Ry
   # Define a function to extract the force from an ASE calculator
   def extract_forces(calc):
      # Return z component of force on final atom (Ry/Bohr)
      return calc.results['forces'][-1, -1]/len(calc.atoms)/units.Ry*units.Bohr

   energy_tol = 2.5e-3/units.Ry # 5 meV/atom in Ry
   force_tol = 5e-3/units.Ry*units.Bohr # 10 meV/Ang in Ry/Bohr


   # Exercise 1a ######################################################################################################
   # Define an array of ecutwfc values to try
   emin = 20
   emax = 150
   ecuts = np.linspace(emin, emax, (emax - emin)//10 + 1)
   # Construct the problem
   exercise_1a = ConvergenceProblem(label='exercise_1a', conv_wrt='ecutwfc', x=ecuts, conv_threshold=energy_tol,
                           extract=extract_energy, from_scratch=from_scratch)
   # Run the calculations
   exercise_1a.run()

   # Plot the result
   exercise_1a.plot(xlabel='ecutwfc (Ry)', ylabel=r'$|\Delta E|$ (Ry/atom)', filename='conv_energy_wrt_ecutwfc')

   # Exercise 1b ######################################################################################################
   # Construct the problem
   exercise_1b = ConvergenceProblem(label='exercise_1b', conv_wrt='ecutwfc', x=ecuts, conv_threshold=force_tol,
                           extract=extract_forces, from_scratch=from_scratch)

   # displace the last atom
   displacement = np.zeros(exercise_1b.master_atoms.positions.shape)
   displacement[-1, -1] += 0.05 * exercise_1b.get_setting('celldm(1)')
   exercise_1b.master_atoms.translate(displacement)

   # Run the calculations
   exercise_1b.run()

   # Plot the result
   exercise_1b.plot(xlabel='ecutwfc (Ry)', ylabel=r'$|\Delta f_z^\mathrm{' + exercise_1b.master_atoms[-1].symbol
                    + '}|$ (Ry/Bohr)', filename='conv_forces_wrt_ecutwfc')

   # Store the results
   CONVERGED_SETTINGS['ecutwfc'] = max([exercise_1a.conv_x, exercise_1b.conv_x]) 
   CONVERGED_SETTINGS['ecutrho'] = 8*max([exercise_1a.conv_x, exercise_1b.conv_x]) 

   # Exercise 1c ######################################################################################################
   # Construct the problem
   exercise_1c = ConvergenceProblem(label='exercise_1c', conv_wrt='kpts', x=[2, 4, 6, 8, 10, 12],
                                    conv_threshold=energy_tol, extract=extract_energy, from_scratch=from_scratch)
   
   # Run the calculations
   exercise_1c.run()

   # Plot the result
   exercise_1c.plot(xlabel='k-point grid', ylabel=r'$|\Delta E|$ (Ry/atom)', filename='conv_energy_wrt_kpts')
   
   # Exercise 1d ######################################################################################################
   # Construct the problem
   exercise_1d = ConvergenceProblem(label='exercise_1d', conv_wrt='kpts', x=[2, 4, 6, 8, 10, 12],
                                    conv_threshold=force_tol, extract=extract_forces, from_scratch=from_scratch)

   # displace the last atom
   displacement = np.zeros(exercise_1d.master_atoms.positions.shape)
   displacement[-1, -1] += 0.05 * exercise_1d.get_setting('celldm(1)')
   exercise_1d.master_atoms.translate(displacement)
   
   # Run the calculations
   exercise_1d.run()

   # Plot the result
   exercise_1d.plot(xlabel='k-point grid', ylabel=r'$|\Delta f_z^\mathrm{' + exercise_1d.master_atoms[-1].symbol
                    + '}|$ (Ry/Bohr)', filename='conv_forces_wrt_kpts')

   # Update the converged parameters
   CONVERGED_SETTINGS['kpts'] = max([exercise_1c.conv_x, exercise_1d.conv_x])

   # Exercise 1e ######################################################################################################
   # Construct the problem
   exercise_1e = FiniteDiffConvergenceProblem(label='exercise_1e', conv_wrt='ecutwfc', x=ecuts, 
                                              conv_threshold=energy_tol, extract=extract_energy,
                                              from_scratch=from_scratch)

   # Run the calculations
   exercise_1e.run()

   # Plot the result
   exercise_1e.plot(xlabel='ecutwfc (Ry)', ylabel=r'$|\Delta E|$ (Ry/atom)', filename='conv_energydiff_wrt_ecutwfc')

   # Update the converged parameters
   if exercise_1e.conv_x > CONVERGED_SETTINGS['ecutwfc']:
      CONVERGED_SETTINGS['ecutwfc'] = exercise_1e.conv_x
      CONVERGED_SETTINGS['ecutrho'] = 8*exercise_1e.conv_x

   # Exercise 2a ######################################################################################################
   # Construct the problem
   v0 = exercise_1a.master_atoms.cell.volume
   exercise_2a = ParabolicBulkModulusProblem(label='exercise_2a', x=v0*np.linspace(0.95, 1.05, 9),
                                             from_scratch=from_scratch)

   # Run the calculations
   exercise_2a.run()

   # Plot the result
   exercise_2a.plot(xlabel='cell volume (Ang^3)', ylabel=r'$E$ (Ry/atom)', filename='fit_parabolic_bulkmodulus')
   
   # Exercise 2b ######################################################################################################
   exercise_2b = BMBulkModulusProblem(label='exercise_2b',
                                      x=np.linspace(0.95, 1.05, 9)*exercise_1a.master_atoms.cell.volume,
                                      from_scratch=from_scratch)

   # Run the calculations (these are identical to 7ab)
   exercise_2b.calculations = copy.deepcopy(exercise_2a.calculations)
   exercise_2b.reload_calculations()

   # Plot the result
   exercise_2b.plot(xlabel='cell volume (Ang^3)', ylabel=r'$E$ (Ry/cell)', filename='fit_birchmurnaghan_bulkmodulus')

   # Converged cell volume
   CONVERGED_SETTINGS['volume_per_atom'] = exercise_2b.eq_lattice_volume / len(exercise_2b.master_atoms)

   # Exercise 3 #######################################################################################################
   for ibrav0 in [False, True]:
      # Determining C_11 and C_12
      if ibrav0:
         label='exercise_3b_c11c12'
      else:
         label='exercise_3a_c11c12'
      exercise_3_ortho = ElasticConstantsC11C12Problem(bulk_modulus=exercise_2b.bulk_modulus, label=label,
                                               master_atoms='../files/NaCl.relax.in',
                                               x=np.linspace(-0.02, 0.02, 9), from_scratch=from_scratch)

      exercise_3_ortho.set_setting('calculation', 'relax')

      if ibrav0:
         exercise_3_ortho.set_setting('ibrav', 0)
         exercise_3_ortho.set_setting('celldm(1)', None)
      else:
         exercise_3_ortho.set_setting('ibrav', 8)

      exercise_3_ortho.run()

      exercise_3_ortho.plot(xlabel='orthorhombic distortion $x$', ylabel=r'$\Delta E$ (Ry/atom)',
                            filename='fit_parabolic_c11_c12')

      # Determining C_44
      if ibrav0:
         label='exercise_3b_c44'
      else:
         label='exercise_3a_c44'
      exercise_3_mono = ElasticConstantsC44Problem(label=label, master_atoms='../files/NaCl.relax.in',
                                           x=np.linspace(-0.02, 0.02, 9), from_scratch=from_scratch)

      exercise_3_mono.set_setting('calculation', 'relax')

      if ibrav0:
         exercise_3_mono.set_setting('ibrav', 0)
         exercise_3_mono.set_setting('celldm(1)', None)
      else:
         exercise_3_mono.set_setting('ibrav', 12)

      exercise_3_mono.run()

      exercise_3_mono.plot(xlabel='monoclinic distortion $x$', ylabel=r'$\Delta E$ (Ry/atom)', filename='fit_parabolic_c44')
