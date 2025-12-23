#!/usr/bin/python3

import pandas as pd

from ase.io import read
from ase.calculators.lj import LennardJones

#from mdeq.parser import argument_parser
from ccm.mdeq.ensemble import nvt,npt,nve
from ccm.mdeq.utils import volume_rescale


def main(args):
	args = vars(args)

	ensemble = args['ensemble'].lower()
	atoms = read(args['input'])
	atoms.calc = LennardJones()

	if (args['scale'] is None) and (args['density'] is not None):
		cell_scale = volume_rescale(atoms,args['density'])
	elif (args['scale'] is not None) and (args['density'] is None):
		cell_scale = args['scale']
	else:
		cell_scale = 1.0

	
	if ensemble.lower() == 'nve':
		print(f'Running {ensemble.upper()}')
		nve(
			atoms,
			dt=args['dt'],
			steps=args['steps'],
			T=args['temperature'],
			cell_scale=cell_scale,
			output_name=args['output'],
			dump_interval=args['dump_interval'],
		)

	elif ensemble.lower() == 'nvt':
		print(f'Running Langevin {ensemble.upper()}')
		nvt(
			atoms,
			dt=args['dt'],
			steps=args['steps'],
			T=args['temperature'],
			cell_scale=cell_scale,
			friction=args['friction'],
			output_name=args['output'],
			dump_interval=args['dump_interval'],
		)
	
	elif ensemble.lower() == 'npt':
		print(f'Running Berendsen {ensemble.upper()}')
		npt(
			atoms,
			dt=args['dt'],
			steps=args['steps'],
			T=args['temperature'],
			pressure=args['pressure'],
			taut=args['taut'],
			taup=args['taup'],
			output_name=args['output'],
			dump_interval=args['dump_interval'],
		)

	elif ensemble.lower() == 'vscan':
		vscan(
			atoms,
			steps=args['steps'],
			min_scale=args['min_scale'],
			max_scale=args['max_scale'],
			output_name=args['output'],
		)

if __name__ == '__main__':
	main()