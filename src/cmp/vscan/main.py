#!/usr/bin/python3

import numpy as np

from ase.io import read,write


def vscan(atoms,mode,min_scale,max_scale,npoints,output_name):
	new_atoms = []
	if mode == 'a':
		print('Atomic mode (atomic coordinates are being scaled)')
	elif mode == 'm':
		print('Molecular mode (atomic coordinates are being scaled relative to molecular centre of mass)')

	for x in np.linspace(min_scale,max_scale,npoints):
		ats = atoms.copy()
		ats.info = atoms.info

		if mode == 'a':
			ats.set_cell(ats.cell*x, scale_atoms=True)
			new_atoms.append(ats)

		elif mode == 'm':
			if 'molID' not in ats.arrays:
				print('Structure has no molIDs! Aborting.')
				quit()
			
			molIDs = set(ats.arrays['molID'])
			com = np.array(
				[
					ats[ats.arrays['molID']==i].get_center_of_mass()*(x-1)
					for i in molIDs
					for _ in range(len(ats[ats.arrays['molID']==i]))
				]
			)
			ats.positions += com
			ats.set_cell(ats.cell*x, scale_atoms=False)
			new_atoms.append(ats)
	
		print(f'Scale = {x:.2f}\tvolume = {ats.get_volume():.3f} Å3')

	if output_name is not None:
		write(output_name,new_atoms)


def main(args):
	args = vars(args)
	
	atoms = read(args['input'])

	vscan(
		atoms,
		mode=args['mode'],
		min_scale = args['min'],
		max_scale = args['max'],
		npoints = args['num_points'],
		output_name=args['output'],
	)