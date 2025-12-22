#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from ase import units
from ase.io import write
from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase.md.langevin import Langevin
from ase.md.nvtberendsen import NVTBerendsen
from ase.md.nptberendsen import NPTBerendsen
from ase.calculators.lj import LennardJones


size = 2
T = 300


atoms = FaceCenteredCubic(
	directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
	symbol='Ar',
	size=(size, size, size),
	pbc=True,
)
print(atoms)

atoms.calc = LennardJones()



def printenergy(a=atoms):  # store a reference to atoms in the definition.
	epot = a.get_potential_energy()/len(a)
	ekin = a.get_kinetic_energy()/len(a)
	print(
		f'Energy per atom: Epot ={epot:6.3f}eV  Ekin = {ekin:.3f}eV '
		f'(T={ekin / (1.5 * units.kB):4.0f}K) Etot = {epot + ekin:.3f}eV'
	)

#input_name = 'argon_start.xyz'
#T = 300
#dt = 1.0
#cell_scale = 1.45
#friction = 0.1
#steps = 10000
#output_name = f'argon_start_{int(T)}K.xyz'

def nvt(input_name,steps,T,output_name,dt,cell_scale,friction):
	dyn = Langevin(atoms, dt*units.fs, temperature_K=T, friction=friction)
	dyn.attach(printenergy, interval=100)

	atoms.set_cell(atoms.cell*cell_scale, scale_atoms=True)
	MaxwellBoltzmannDistribution(atoms, temperature_K=T)

	printenergy()
	dyn.run(steps)
	if output_name is not None:
		write(output_name,atoms)