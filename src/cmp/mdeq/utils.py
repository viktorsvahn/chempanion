#!/usr/bin/python3

from ase import units

def printenergy(a):  # store a reference to atoms in the definition.
	epot = a.get_potential_energy()/len(a)
	ekin = a.get_kinetic_energy()/len(a)
	volume = a.get_volume()/(units.m**3)
	mass = sum(a.get_masses())/units.kg
	print(
		f'Energy per atom: Epot ={epot:6.3f} eV  Ekin = {ekin:.3f} eV '
		f'(T={ekin / (1.5 * units.kB):4.0f} K) Etot = {epot + ekin:.3f} eV '
		f'density = {mass/volume:.4} kg/m3'
	)

def volume_rescale(atoms,density):
	from ase import units
	volume = atoms.get_volume()/(units.m**3)
	mass = atoms.get_masses().sum()/units.kg
	rho = mass/volume
	new_volume = mass/density
	scale_factor = (new_volume/volume)**(1/3)
	return scale_factor
