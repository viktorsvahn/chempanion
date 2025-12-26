#!/usr/bin/python3

import pandas as pd

from ase.io import read
from ase.calculators.lj import LennardJones

from cmp.utils import show_small_banner
from cmp.mdeq.ensemble import nvt,npt,nve
from cmp.mdeq.utils import volume_rescale


def main(args):
	args = vars(args)

	ensemble = args['ensemble'].lower()
	atoms = read(args['input'])
	atoms.calc = LennardJones()

	if (args['vscale'] is None) and (args['density'] is not None):
		vscale = volume_rescale(atoms,args['density'])
	elif (args['vscale'] is not None) and (args['density'] is None):
		vscale = args['vscale']
	else:
		vscale = 1.0

	
	show_small_banner()
	if ensemble.lower() == 'nve':
		print(f'Running {ensemble.upper()}')
		nve(
			atoms,
			dt=args['dt'],
			steps=args['steps'],
			T=args['temperature'],
			vscale=vscale,
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
			vscale=vscale,
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