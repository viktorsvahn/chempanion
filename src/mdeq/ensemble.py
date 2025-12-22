#!/usr/bin/python3

import numpy as np

from ase import units
from ase.io import read, write
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase.md.langevin import Langevin
from ase.md.nvtberendsen import NVTBerendsen
from ase.md.nptberendsen import NPTBerendsen

from mdeq.utils import printenergy


def nve(atoms,steps,T,output_name,dt,cell_scale,dump_interval):
	dyn = VelocityVerlet(atoms, dt*units.fs)
	dyn.attach(printenergy, interval=dump_interval,**dict(a=atoms))

	atoms.set_cell(atoms.cell*cell_scale, scale_atoms=True)
	MaxwellBoltzmannDistribution(atoms, temperature_K=T)

	dyn.run(steps)
	if output_name is not None:
		write(output_name,atoms)


def nvt(atoms,steps,T,output_name,dt,cell_scale,friction,dump_interval):
	dyn = Langevin(atoms, dt*units.fs, temperature_K=T, friction=friction)
	dyn.attach(printenergy, interval=dump_interval,**dict(a=atoms))

	atoms.set_cell(atoms.cell*cell_scale, scale_atoms=True)
	MaxwellBoltzmannDistribution(atoms, temperature_K=T)

	dyn.run(steps)
	if output_name is not None:
		write(output_name,atoms)


def npt(atoms,steps,T,output_name,dt,pressure,taut,taup,dump_interval):
	Z = pressure*atoms.get_volume()/(units.kB*len(atoms)*T)
	dyn = NPTBerendsen(
		atoms,
		dt*units.fs,
		temperature_K=T,
		pressure_au=pressure*units.bar,
		taut=taut,
		taup=taup,
		compressibility_au=Z,
	)
	dyn.attach(printenergy, interval=dump_interval,**dict(a=atoms))
	MaxwellBoltzmannDistribution(atoms, temperature_K=T)

	dyn.run(steps)
	if output_name is not None:
		write(output_name,atoms)